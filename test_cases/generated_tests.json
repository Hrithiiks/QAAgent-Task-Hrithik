```json
{
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Create Interview with Job Description",
      "description": "Verify the functionality of creating an interview using a provided job description.",
      "category": "Interview Creation",
      "priority": "High",
      "steps": [
        {
          "action": "visit",
          "selector": "https://[your-application-url]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview']"
        },
        {
          "action": "input",
          "selector": "[name='jobDescription']",
          "value": "[Your Job Description]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview-button']"
        }
      ]
    },
    {
      "id": "TC-002",
      "title": "Create Interview with Enhanced Job Description",
      "description": "Verify the functionality of creating an interview using the enhanced job description feature.",
      "category": "Interview Creation",
      "priority": "High",
      "steps": [
        {
          "action": "visit",
          "selector": "https://[your-application-url]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview']"
        },
        {
          "action": "input",
          "selector": "[name='jobTitle']",
          "value": "[Your Job Title]"
        },
        {
          "action": "click",
          "selector": "[data-testid='generate-jd-button']"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview-button']"
        }
      ]
    },
    {
      "id": "TC-003",
      "title": "Customize Interview Questions",
      "description": "Verify the ability to customize interview questions after AI suggestion.",
      "category": "Interview Customization",
      "priority": "Medium",
      "steps": [
        {
          "action": "visit",
          "selector": "https://[your-application-url]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview']"
        },
        {
          "action": "input",
          "selector": "[name='jobDescription']",
          "value": "[Your Job Description]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview-button']"
        },
        {
          "action": "click",
          "selector": "[data-testid='edit-question-button']"
        },
        {
          "action": "input",
          "selector": "[name='questionText']",
          "value": "[Modified Question Text]"
        }
      ]
    },
    {
      "id": "TC-004",
      "title": "Verify Public Interview Link Generation",
      "description": "Verify that a unique public interview link is generated upon interview creation.",
      "category": "Interview Creation",
      "priority": "Medium",
      "steps": [
        {
          "action": "visit",
          "selector": "https://[your-application-url]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview']"
        },
        {
          "action": "input",
          "selector": "[name='jobDescription']",
          "value": "[Your Job Description]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview-button']"
        },
        {
          "action": "get_text",
          "selector": "[data-testid='public-link']",
          "variable": "interviewLink"
        }
      ]
    },
    {
      "id": "TC-005",
      "title": "Verify Resume Screening with Threshold",
      "description": "Verify the functionality of resume screening based on a set threshold.",
      "category": "Candidate Screening",
      "priority": "High",
      "steps": [
        {
          "action": "visit",
          "selector": "https://[your-application-url]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview']"
        },
        {
          "action": "input",
          "selector": "[name='jobDescription']",
          "value": "[Your Job Description]"
        },
        {
          "action": "click",
          "selector": "[data-testid='create-interview-button']"
        },
        {
          "action": "upload_file",
          "selector": "[data-testid='resume-upload']",
          "path": "[Path to Candidate Resume]"
        }
      ]
    },
    {
      "id": "TC-006",
      "title": "Verify Video Interview Functionality",
      "description": "Verify the functionality of the video interview stage.",
      "category": "Candidate Screening",
      "priority": "High",
      "steps": [
        {
          "action": "visit",
          "selector": "[data-testid='responses']"
        },
        {
          "action": "click",
          "selector": "[data-testid='video-interview-link']"
        }
      ]
    },
    {
      "id": "TC-007",
      "title": "Verify Candidate Review Section",
      "description": "Verify the functionality of the candidate review section.",
      "category": "Candidate Management",
      "priority": "Medium",
      "steps": [
        {
          "action": "visit",
          "selector": "https://[your-application-url]"
        },
        {
          "action": "click",
          "selector": "[data-testid='responses']"
        }
      ]
    }
  ]
}
```