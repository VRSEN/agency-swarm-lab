TASK_TEMPLATE = {
    "Task name": {
        "id": "title",
        "type": "title",
        "title": [
            {
                "type": "text",
                "text": {"content": "Placeholder title", "link": None},
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default",
                },
                "plain_text": "Placeholder title",
                "href": None,
            }
        ],
    },
    # Set status to Backlog
    "Status": {
        "id": "notion%3A%2f%2ftasks%2fstatus_property",
        "type": "status",
        "status": {"id": "vDa;", "name": "Backlog", "color": "gray"},
    },
    "Project": {
        "id": "notion%3A%2f%2ftasks%2ftask_to_project_relation",
        "type": "relation",
        "relation": [{"id": "placeholder-id"}],
        "has_more": False,
    },
}

BACKGROUND_PLACEHOLDER = [
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "🌐 Background:",
                        "link": None,
                    },
                    "annotations": {
                        "bold": True,
                    },
                }
            ]
        },
    }
]
