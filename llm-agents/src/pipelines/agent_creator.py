#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.


from steps.agent_creator import agent_creator
from steps.index_generator import index_generator
from steps.url_scraper import url_scraper
from steps.web_url_loader import web_url_loader
from zenml import pipeline, Model
from zenml.config import DockerSettings
from zenml.integrations.constants import LANGCHAIN, OPEN_AI, PILLOW

PIPELINE_NAME = "zenml_agent_creation_pipeline"

docker_settings = DockerSettings(
    requirements="requirements.txt",
    required_integrations=[LANGCHAIN, OPEN_AI, PILLOW],
)

@pipeline(name=PIPELINE_NAME,
          enable_cache=True,
          settings={"docker": docker_settings},
          model=Model(
              name="zenml_agent",
              license="Apache",
              description="ZenML Agent with a vector store tool.",
              tags=["llm", "agent", "rag"]
          ))
def docs_to_agent_pipeline(
    docs_url: str = "",
    repo_url: str = "",
    release_notes_url: str = "",
    website_url: str = "",
) -> None:
    """Generate index for ZenML.

    Args:
        docs_url: URL to the documentation.
        repo_url: URL to the repository.
        release_notes_url: URL to the release notes.
        website_url: URL to the website.
    """
    urls = url_scraper(docs_url, repo_url, release_notes_url, website_url)
    documents = web_url_loader(urls)
    vector_store = index_generator(documents)
    agent = agent_creator(vector_store=vector_store)