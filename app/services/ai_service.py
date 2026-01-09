import asyncio
import logging
import json
from pathlib import Path
from typing import List, Dict, Any

from app.config import settings
from app.core.semaphore import semaphore_manager
from app.core.exceptions import AIServiceError
from app.utils.retry import ai_retry

logger = logging.getLogger(__name__)


class AIService:
    """AI-powered code analysis using Map-Reduce pattern"""

    def __init__(self):
        self.provider = settings.llm_provider

        if self.provider == "openai":
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
        elif self.provider == "ollama":
            import ollama
            self.client = ollama.AsyncClient(host=settings.ollama_base_url)
            self.model = settings.ollama_model
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        logger.info(f"AIService initialized with provider: {self.provider}, model: {self.model}")

    async def map_analysis(
        self,
        file_groups: List[List[Dict[str, any]]],
        workspace_path: str
    ) -> List[Dict[str, Any]]:
        """
        Phase 1: Map - Analyze individual file groups in parallel

        Args:
            file_groups: List of file groups (each group is a list of related files)
            workspace_path: Path to the cloned repository

        Returns:
            List of analysis results for each group
        """
        logger.info(f"Starting Map analysis for {len(file_groups)} file groups")

        # Create tasks for parallel processing (with internal semaphore)
        tasks = [
            self._analyze_file_group(group, workspace_path)
            for group in file_groups
        ]

        # Execute all tasks concurrently (limited by internal semaphore)
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Map analysis failed for group {i}: {result}")
            else:
                valid_results.append(result)

        logger.info(f"Map analysis completed: {len(valid_results)}/{len(file_groups)} succeeded")
        return valid_results

    async def _analyze_file_group(
        self,
        file_group: List[Dict[str, any]],
        workspace_path: str
    ) -> Dict[str, Any]:
        """
        Analyze a single file group with internal semaphore control

        Args:
            file_group: List of related files
            workspace_path: Repository workspace path

        Returns:
            Analysis result for this group
        """
        # Acquire internal semaphore
        await semaphore_manager.acquire_internal()

        try:
            # Extract user's code lines only (not reading entire file)
            files_content = []
            for file_info in file_group:
                try:
                    # Build content from user's code lines only
                    user_code = "\n".join(
                        line["code"] for line in file_info["user_code_lines"]
                    )

                    files_content.append({
                        "path": file_info["file_path"],
                        "content": user_code,
                        "user_lines": file_info["user_lines"]
                    })
                except Exception as e:
                    logger.warning(f"Failed to extract user code from {file_info['file_path']}: {e}")

            if not files_content:
                return {"error": "No files could be read"}

            # Build prompt
            prompt = self._build_map_prompt(files_content)

            # Call AI API with retry
            result = await self._call_ai_api(prompt, is_map=True)

            return result

        finally:
            # Always release semaphore
            semaphore_manager.release_internal()

    def _build_map_prompt(self, files_content: List[Dict[str, str]]) -> str:
        """
        Build XML-formatted prompt for Map phase

        Format:
        <documents>
          <document>
            <path>file/path.java</path>
            <user_lines>25</user_lines>
            <content>
            ... code ...
            </content>
          </document>
        </documents>
        """
        xml_parts = ["<documents>"]

        for file_data in files_content:
            xml_parts.append("  <document>")
            xml_parts.append(f"    <path>{file_data['path']}</path>")
            xml_parts.append(f"    <user_lines>{file_data['user_lines']}</user_lines>")
            xml_parts.append("    <content>")
            xml_parts.append(file_data['content'])
            xml_parts.append("    </content>")
            xml_parts.append("  </document>")

        xml_parts.append("</documents>")

        return "\n".join(xml_parts)

    async def reduce_analysis(
        self,
        map_results: List[Dict[str, Any]],
        project_tree: str
    ) -> Dict[str, Any]:
        """
        Phase 2: Reduce - Synthesize all map results into final report

        Args:
            map_results: List of individual file group analyses
            project_tree: Full project directory tree structure

        Returns:
            Final analysis result matching AnalysisResult schema
        """
        logger.info(f"Starting Reduce analysis with {len(map_results)} map results")

        # Build reduce prompt
        prompt = self._build_reduce_prompt(map_results, project_tree)

        # Call AI API
        result = await self._call_ai_api(prompt, is_map=False)

        logger.info("Reduce analysis completed")
        return result

    def _build_reduce_prompt(
        self,
        map_results: List[Dict[str, Any]],
        project_tree: str
    ) -> str:
        """Build prompt for Reduce phase"""
        prompt_parts = []

        # Add project tree for context
        prompt_parts.append("=== PROJECT STRUCTURE ===")
        prompt_parts.append(project_tree)
        prompt_parts.append("")

        # Add map results
        prompt_parts.append("=== CODE ANALYSIS SUMMARIES ===")
        for i, result in enumerate(map_results, 1):
            prompt_parts.append(f"\n--- Analysis {i} ---")
            prompt_parts.append(json.dumps(result, ensure_ascii=False, indent=2))

        return "\n".join(prompt_parts)

    @ai_retry
    async def _call_ai_api(self, prompt: str, is_map: bool) -> Dict[str, Any]:
        """
        Call AI API with appropriate system prompt

        Args:
            prompt: User prompt content
            is_map: True for Map phase, False for Reduce phase

        Returns:
            Parsed JSON response

        Raises:
            AIServiceError: If API call fails
        """
        try:
            system_prompt = self._get_system_prompt(is_map)

            if self.provider == "openai":
                response = await self._call_openai(system_prompt, prompt)
            else:  # ollama
                response = await self._call_ollama(system_prompt, prompt)

            # Parse JSON response
            return self._parse_ai_response(response, is_map)

        except Exception as e:
            raise AIServiceError(f"AI API call failed: {e}")

    async def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content

    async def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Call Ollama API"""
        response = await self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={
                "temperature": 0.3,
                "num_predict": 2000
            }
        )
        return response['message']['content']

    def _get_system_prompt(self, is_map: bool) -> str:
        """Get appropriate system prompt for Map or Reduce phase"""
        if is_map:
            return """You are a Senior Code Reviewer.

**IMPORTANT**: You are analyzing ONLY the code lines written by the target user.
The <content> section contains EXCLUSIVELY the code that this specific user contributed.
Do NOT assume there is other code - you are seeing the complete contribution of this user in these files.

Analyze the provided code in XML format and provide a concise summary in JSON format:
{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "Main features implemented by this developer (1-2 sentences, English)",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "Notable code patterns or design (1-2 sentences, English)"
}

**IMPORTANT**: Use English for all text fields. Be concise and focus on what THIS USER's code does."""

        else:  # Reduce
            return """You are a Tech Lead preparing a portfolio report.

You are given:
1. PROJECT STRUCTURE: Full directory tree of the project
2. CODE ANALYSIS SUMMARIES: Individual analyses of code chunks

Synthesize this information into a structured report in strict JSON format.

**IMPORTANT**: Your response MUST be valid JSON only. No markdown, no explanations, just JSON.

Output JSON schema:
{
  "summary": "이 개발자의 전체 기여도와 주요 작업 내용 (한글, 3-5 문장)",
  "tech_stack": ["Java", "Spring Boot", "Redis", "WebSocket"],
  "key_contributions": [
    "기여 내용 1 (구체적으로, 한글)",
    "기여 내용 2",
    "기여 내용 3"
  ],
  "code_quality": "코드 품질 평가 (설계 패턴, 원칙 준수 등, 한글, 2-3 문장)",
  "project_tree": "COPY THE EXACT PROJECT STRUCTURE PROVIDED"
}

Return ONLY valid JSON. No markdown code blocks."""

    def _parse_ai_response(self, response: str, is_map: bool) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        try:
            # Remove markdown code blocks if present
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            # Parse JSON
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Response was: {response}")

            # Return fallback structure
            if is_map:
                return {
                    "files_analyzed": [],
                    "main_features": "분석 실패",
                    "tech_stack": [],
                    "notable_patterns": "응답 파싱 오류"
                }
            else:
                return {
                    "summary": "분석 결과를 파싱하는 중 오류가 발생했습니다.",
                    "tech_stack": [],
                    "key_contributions": [],
                    "code_quality": "평가 불가",
                    "project_tree": ""
                }
