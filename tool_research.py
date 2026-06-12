from datetime import datetime

AI_TOOLS = [
    {
        "title": "Best AI Writing Tools for Small Business Owners",
        "keyword": "AI writing tools for small business",
        "tool_name": "AI Writing Tools",
        "audience": "small business owners",
        "problem": "creating daily content without hiring a writer",
    },
    {
        "title": "Best AI Design Tools for Content Creators",
        "keyword": "AI design tools for content creators",
        "tool_name": "AI Design Tools",
        "audience": "content creators",
        "problem": "making social media graphics faster",
    },
    {
        "title": "Best AI Automation Tools for Online Businesses",
        "keyword": "AI automation tools for online business",
        "tool_name": "AI Automation Tools",
        "audience": "online business owners",
        "problem": "saving time on repetitive tasks",
    },
]


def get_ai_tool_topic():
    today_index = datetime.now().timetuple().tm_yday % len(AI_TOOLS)
    return AI_TOOLS[today_index]
