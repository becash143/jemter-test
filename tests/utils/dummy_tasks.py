DUMMY_TASKS = [
    {"text": "sample task 1"},
    {"text": "sample task 2"},
    {"text": "sample task 2"},
    {"text": "sample task 2"},
    {"text": "sample task 1"},
    {"text": "sample task 3"},
    {"text": "sample task 3"},
]

DUMMY_TASKS_FOR_AL = [
    {
        "text": "William Henry Gates III (born October 28, 1955) is an American business magnate, software developer, investor, and philanthropist. He is best known as the co-founder of Microsoft Corporation. During his career at Microsoft, Gates held the positions of chairman, chief executive officer (CEO), president and chief software architect, while also being the largest individual shareholder until May 2014. He is one of the best-known entrepreneurs and pioneers of the microcomputer revolution of the 1970s and 1980s. Born and raised in Seattle, Washington, Gates co-founded Microsoft with childhood friend Paul Allen in 1975, in Albuquerque, New Mexico; it went on to become the world's largest personal computer software company. Gates led the company as chairman and CEO until stepping down as CEO in January 2000, but he remained chairman and became chief software architect. During the late 1990s, Gates had been criticized for his business tactics, which have been considered anti-competitive. This opinion has been upheld by numerous court rulings. In June 2006, Gates announced that he would be transitioning to a part-time role at Microsoft and full-time work at the Bill & Melinda Gates Foundation, the private charitable foundation that he and his wife, Melinda Gates, established in 2000. He gradually transferred his duties to Ray Ozzie and Craig Mundie. He stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella."
    },
    {"text": "sample task 1"},
]

USER_WISE_STATUS_COMPLETIONS = [
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-04-19T05:23:55.724Z",
                "lead_time": 7,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "X7Np7kQ9Kv",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 1001,
                "submitted_at": "2021-04-19T10:53:57.973",
                "updated_at": "2021-04-19T05:23:58.000026Z",
                "updated_by": "collaborate",
            },
            {
                "created_username": "readonly",
                "created_ago": "2021-04-19T05:26:28.536Z",
                "lead_time": 5,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "qxdvEDgQql",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 1002,
                "submitted_at": "2021-04-19T10:56:30.321",
                "updated_at": "2021-04-19T05:26:30.359240Z",
                "updated_by": "readonly",
                "review_status": {
                    "approved": True,
                    "comment": "Nice",
                    "reviewer": "reviewer",
                    "reviewed_at": "2021-04-19T05:26:54.851Z",
                },
            },
        ],
        "predictions": [],
        "created_at": "2021-04-19 05:28:41",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": "C-Submitted R- Reviewed",
        },
        "id": 2,
    },
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-04-19T05:23:45.861Z",
                "lead_time": 4,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "Id_7uDXejb",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": False,
                "id": 2001,
            },
            {
                "created_username": "readonly",
                "created_ago": "2021-04-19T05:26:14.746Z",
                "lead_time": 7,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "CO1xl9MJO9",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 2002,
                "submitted_at": "2021-04-19T10:56:17.304",
                "updated_at": "2021-04-19T05:26:17.338964Z",
                "updated_by": "readonly",
            },
        ],
        "predictions": [],
        "created_at": "2021-04-19 05:28:41",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": "C-Inprogress R-Submitted",
        },
        "id": 1,
    },
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-04-19T05:24:07.956Z",
                "lead_time": 8,
                "result": [
                    {
                        "value": {
                            "start": 3,
                            "end": 7,
                            "text": "have",
                            "labels": ["PERSON"],
                        },
                        "id": "3xFO3SQzlL",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 3001,
                "submitted_at": "2021-04-19T10:54:17.271",
                "updated_at": "2021-04-19T05:24:17.301853Z",
                "updated_by": "collaborate",
                "review_status": {
                    "approved": True,
                    "comment": "Good",
                    "reviewer": "reviewer",
                    "reviewed_at": "2021-04-19T05:25:31.092Z",
                },
            },
            {
                "created_username": "readonly",
                "created_ago": "2021-04-19T05:32:04.296Z",
                "lead_time": 4,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "HVOXjflkXZ",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": False,
                "id": 3002,
            },
        ],
        "predictions": [],
        "created_at": "2021-04-19 05:28:41",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": "C-Reviewed R-Inprogress",
        },
        "id": 3,
    },
]

DUMMY_TASK_FOR_NEXT_COMPLETION = [
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-09-09T12:17:27.391Z",
                "lead_time": 7,
                "result": [
                    {
                        "value": {
                            "start": 8,
                            "end": 11,
                            "text": "DEF",
                            "labels": ["CARDINAL"],
                        },
                        "id": "AXYDwBtWma",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 1001,
                "updated_at": "2021-09-09T12:18:36.167514Z",
                "updated_by": "collaborate",
                "submitted_at": "2021-09-09T18:03:35.713",
            }
        ],
        "predictions": [],
        "created_at": "2021-09-09 12:17:27",
        "created_by": "collaborate",
        "data": {"text": "This is DEF task", "title": ""},
        "id": 1,
    },
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-09-09T12:17:49.989Z",
                "lead_time": 10,
                "result": [
                    {
                        "value": {
                            "start": 8,
                            "end": 11,
                            "text": "JKL",
                            "labels": ["CARDINAL"],
                        },
                        "id": "GjvjL58fvD",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 3001,
                "updated_at": "2021-09-09T12:19:19.181066Z",
                "updated_by": "collaborate",
                "submitted_at": "2021-09-09T18:04:18.635",
            }
        ],
        "predictions": [],
        "created_at": "2021-09-09 12:17:50",
        "created_by": "collaborate",
        "data": {"text": "This is JKL task", "title": ""},
        "id": 3,
    },
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-09-09T12:17:35.815Z",
                "lead_time": 31,
                "result": [
                    {
                        "value": {
                            "start": 8,
                            "end": 11,
                            "text": "GHI",
                            "labels": ["CARDINAL"],
                        },
                        "id": "bBx4BOoajs",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 2001,
                "updated_at": "2021-09-09T12:19:09.115353Z",
                "updated_by": "collaborate",
                "submitted_at": "2021-09-09T18:04:08.660",
            }
        ],
        "predictions": [],
        "created_at": "2021-09-09 12:17:36",
        "created_by": "collaborate",
        "data": {"text": "This is GHI task", "title": ""},
        "id": 2,
    },
    {"text": "This is ABC task"},
    {"text": "This is MNO task"},
    {"text": "This is PQR task"},
    {"text": "This is STU task"},
]

DUMMY_SUBMITTED_TASK = [
    {
        "completions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-04-19T05:23:55.724Z",
                "lead_time": 7,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "X7Np7kQ9Kv",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 1001,
                "submitted_at": "2021-04-19T10:53:57.973",
                "updated_at": "2021-04-19T05:23:58.000026Z",
                "updated_by": "collaborate",
            }
        ],
        "predictions": [],
        "created_at": "2021-04-19 05:28:41",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": "C-Submitted R- Reviewed",
        },
        "id": 1,
    }
]

DUMMY_PREDICTION_TASK = [
    {
        "predictions": [
            {
                "created_username": "collaborate",
                "created_ago": "2021-04-19T05:23:55.724Z",
                "lead_time": 7,
                "result": [
                    {
                        "value": {
                            "start": 0,
                            "end": 2,
                            "text": "To",
                            "labels": ["PERSON"],
                        },
                        "id": "X7Np7kQ9Kv",
                        "from_name": "label",
                        "to_name": "text",
                        "type": "labels",
                    }
                ],
                "honeypot": True,
                "id": 1001,
                "submitted_at": "2021-04-19T10:53:57.973",
                "updated_at": "2021-04-19T05:23:58.000026Z",
                "updated_by": "collaborate",
            }
        ],
        "created_at": "2021-04-19 05:28:41",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
        }
    }
]