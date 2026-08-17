import os
import requests
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# YouTube Configuration
# ============================================================

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_SEARCH_URL = (
    "https://www.googleapis.com/youtube/v3/search"
)


# ============================================================
# Search YouTube
# ============================================================

def search_youtube(
    query,
    max_results=5
):
    """
    Search YouTube for videos related to a task/topic.
    """

    if not YOUTUBE_API_KEY:
        return []

    try:

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "order": "relevance",
            "regionCode": "IN",
            "relevanceLanguage": "en",
            "safeSearch": "moderate",
        }

        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        videos = []

        for item in data.get("items", []):

            video_id = (
                item
                .get("id", {})
                .get("videoId")
            )

            snippet = item.get(
                "snippet",
                {}
            )

            if not video_id:
                continue

            videos.append(
                {
                    "id": video_id,
                    "title": snippet.get(
                        "title",
                        "YouTube Video"
                    ),
                    "description": snippet.get(
                        "description",
                        ""
                    ),
                    "channel": snippet.get(
                        "channelTitle",
                        ""
                    ),
                    "thumbnail": (
                        snippet
                        .get("thumbnails", {})
                        .get("medium", {})
                        .get("url")
                    ),
                    "url": (
                        f"https://www.youtube.com/watch?v="
                        f"{video_id}"
                    ),
                }
            )

        return videos

    except Exception as e:

        print(
            f"YouTube search error: {e}"
        )

        return []


# ============================================================
# YouTube Search Link Fallback
# ============================================================

def youtube_search_link(query):

    return (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )


# ============================================================
# LeetCode Search
# ============================================================

def get_leetcode_resources(topic):

    encoded_topic = quote_plus(topic)

    return {
        "problemset": (
            "https://leetcode.com/problemset/"
        ),
        "search": (
            "https://leetcode.com/problemset/?search="
            + encoded_topic
        ),
        "topic_search": (
            "https://leetcode.com/problemset/"
            "?search="
            + encoded_topic
        ),
    }


# ============================================================
# Detect Resource Type
# ============================================================

def detect_resource_type(
    title,
    description=""
):

    text = (
        f"{title} {description}"
        .lower()
    )

    # --------------------------------------------------------
    # Programming
    # --------------------------------------------------------

    programming_keywords = [
        "leetcode",
        "coding",
        "programming",
        "algorithm",
        "data structure",
        "dsa",
        "java",
        "python",
        "javascript",
        "react",
        "spring boot",
        "sql",
        "database",
        "oops",
        "dynamic programming",
        "array",
        "string",
        "linked list",
        "tree",
        "graph",
        "binary search",
    ]

    if any(
        keyword in text
        for keyword in programming_keywords
    ):

        return "coding"

    # --------------------------------------------------------
    # Fitness
    # --------------------------------------------------------

    fitness_keywords = [
        "gym",
        "workout",
        "exercise",
        "fitness",
        "muscle",
        "chest",
        "back workout",
        "leg workout",
        "shoulder",
        "biceps",
        "triceps",
        "cardio",
        "weight training",
    ]

    if any(
        keyword in text
        for keyword in fitness_keywords
    ):

        return "fitness"

    # --------------------------------------------------------
    # Study
    # --------------------------------------------------------

    study_keywords = [
        "study",
        "learn",
        "revision",
        "exam",
        "college",
        "dbms",
        "os",
        "operating system",
        "computer network",
        "software engineering",
        "mathematics",
    ]

    if any(
        keyword in text
        for keyword in study_keywords
    ):

        return "study"

    return "general"


# ============================================================
# Generate Resource Query
# ============================================================

def generate_resource_query(
    title,
    description="",
    category=None
):

    resource_type = detect_resource_type(
        title,
        description
    )

    task_text = (
        f"{title} {description}"
    ).strip()

    # --------------------------------------------------------
    # Fitness
    # --------------------------------------------------------

    if resource_type == "fitness":

        return {
            "type": "fitness",
            "youtube_query": (
                f"{task_text} workout "
                f"beginner proper form"
            ),
            "leetcode": None,
        }

    # --------------------------------------------------------
    # Coding
    # --------------------------------------------------------

    if resource_type == "coding":

        return {
            "type": "coding",
            "youtube_query": (
                f"{task_text} tutorial "
                f"problem solving"
            ),
            "leetcode": get_leetcode_resources(
                task_text
            ),
        }

    # --------------------------------------------------------
    # Study
    # --------------------------------------------------------

    if resource_type == "study":

        return {
            "type": "study",
            "youtube_query": (
                f"{task_text} complete tutorial "
                f"lecture"
            ),
            "leetcode": None,
        }

    # --------------------------------------------------------
    # General
    # --------------------------------------------------------

    return {
        "type": "general",
        "youtube_query": (
            f"{task_text} tutorial guide"
        ),
        "leetcode": None,
    }


# ============================================================
# Get Resources For Task
# ============================================================

def get_task_resources(task):

    title = getattr(
        task,
        "title",
        ""
    )

    description = getattr(
        task,
        "description",
        ""
    )

    resource_info = generate_resource_query(
        title,
        description
    )

    youtube_videos = search_youtube(
        resource_info["youtube_query"],
        max_results=5
    )

    return {
        "type": resource_info["type"],
        "youtube_query": resource_info[
            "youtube_query"
        ],
        "youtube_videos": youtube_videos,
        "youtube_search": youtube_search_link(
            resource_info["youtube_query"]
        ),
        "leetcode": resource_info["leetcode"],
    }