import os
import logging

import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# ============================================================
# LOGGING & ENVIRONMENT SETUP
# ============================================================

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

# ============================================================
# TOOL: SAVE USER QUERY TO STATE
# ============================================================

def save_user_query(
    tool_context: ToolContext,
    query: str
) -> dict[str, str]:
    """
    Saves the user's query into shared state.
    """

    tool_context.state["USER_QUERY"] = query

    logging.info(
        f"[STATE] USER_QUERY saved: {query}"
    )

    return {
        "status": "success"
    }

# ============================================================
# WIKIPEDIA TOOL
# ============================================================

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(
            top_k_results=5,
            doc_content_chars_max=5000
        )
    )
)

# ============================================================
# AGENT 1: SPACE & COSMOLOGY RESEARCHER
# ============================================================

space_research_agent = Agent(
    name="space_research_agent",
    model=model_name,
    description="""
    Expert researcher for astronomy,
    astrophysics, cosmology and the universe.
    """,
    instruction="""
    You are a world-class astrophysicist.

    Research the USER_QUERY and provide findings about:

    - Universe
    - Big Bang
    - Cosmology
    - Stars
    - Galaxies
    - Nebulae
    - Black Holes
    - Dark Matter
    - Dark Energy
    - Exoplanets
    - Solar System
    - Astronomy

    Use available tools when needed.

    USER QUERY:
    {USER_QUERY}
    """,
    tools=[wikipedia_tool],
    output_key="space_research"
)

# ============================================================
# AGENT 2: SPACE MISSIONS EXPERT
# ============================================================

mission_agent = Agent(
    name="mission_agent",
    model=model_name,
    description="""
    Researches space missions,
    spacecraft, astronauts,
    and space agencies.
    """,
    instruction="""
    You are a space mission specialist.

    Research information related to:

    - NASA
    - ESA
    - ISRO
    - JAXA
    - SpaceX
    - Blue Origin
    - Artemis Program
    - Apollo Missions
    - Voyager Missions
    - Mars Missions
    - Lunar Missions
    - Satellites
    - Spacecraft
    - Astronauts

    USER QUERY:
    {USER_QUERY}

    Use tools if mission information is needed.
    """,
    tools=[wikipedia_tool],
    output_key="mission_research"
)

# ============================================================
# AGENT 3: EXTRATERRESTRIAL LIFE EXPERT
# ============================================================

extraterrestrial_agent = Agent(
    name="extraterrestrial_agent",
    model=model_name,
    description="""
    Researches extraterrestrial life,
    SETI, habitability,
    and astrobiology.
    """,
    instruction="""
    You are an astrobiology researcher.

    Research:

    - Extraterrestrial life
    - Alien civilizations
    - SETI
    - Drake Equation
    - Fermi Paradox
    - Biosignatures
    - Technosignatures
    - Habitable Exoplanets
    - Astrobiology

    IMPORTANT:
    - Use scientific evidence.
    - Clearly distinguish facts from theories.
    - Avoid unsupported speculation.

    USER QUERY:
    {USER_QUERY}
    """,
    tools=[wikipedia_tool],
    output_key="et_research"
)

# ============================================================
# AGENT 4: RESPONSE SYNTHESIZER
# ============================================================

response_formatter = Agent(
    name="cosmic_response_formatter",
    model=model_name,
    description="""
    Produces final user-facing response.
    """,
    instruction="""
    You are Cosmic Navigator.

    Combine all available information.

    SPACE RESEARCH:
    {space_research}

    MISSION RESEARCH:
    {mission_research}

    EXTRATERRESTRIAL RESEARCH:
    {et_research}

    Create a comprehensive response that:

    - Is scientifically accurate.
    - Uses markdown formatting.
    - Explains complex ideas clearly.
    - Includes relevant mission details.
    - Includes astronomy context.
    - Includes extraterrestrial context if applicable.
    - Notes uncertainty where appropriate.
    - Avoids hallucinations.

    Format:

    ## Overview

    ## Key Findings

    ## Scientific Context

    ## Interesting Facts

    ## Summary

    End with:

    "🚀 Would you like to explore another cosmic topic?"
    """
)

# ============================================================
# WORKFLOW
# ============================================================

cosmic_workflow = SequentialAgent(
    name="cosmic_workflow",
    description="""
    Main workflow for cosmic research.
    """,
    sub_agents=[
        space_research_agent,
        mission_agent,
        extraterrestrial_agent,
        response_formatter
    ]
)

# ============================================================
# ROOT AGENT
# ============================================================

root_agent = Agent(
    name="cosmic_navigator",
    model=model_name,
    description="""
    Cosmic Navigator is an AI expert in:

    - Astronomy
    - Astrophysics
    - Cosmology
    - Space Exploration
    - Space Missions
    - Spacecraft
    - Astronauts
    - Extraterrestrial Life
    - Astrobiology
    - The Universe
    """,
    instruction="""
    You are Cosmic Navigator.

    Your role is to help users explore:

    - Space
    - Cosmos
    - Universe
    - Astronomy
    - Cosmology
    - Space Missions
    - Rockets
    - Satellites
    - Astronauts
    - Space Agencies
    - Alien Life
    - Astrobiology
    - Exoplanets
    - Black Holes
    - Galaxies
    - Scientific Discoveries

    STEP 1:
    Use the save_user_query tool to store the user's query.

    STEP 2:
    Transfer control to the cosmic_workflow.

    Always maintain scientific accuracy.
    Never invent facts.
    Clearly state uncertainty when information is incomplete.
    """,
    tools=[
        save_user_query
    ],
    sub_agents=[
        cosmic_workflow
    ]
)