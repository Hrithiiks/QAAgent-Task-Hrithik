import json
import os
import re

JSON_INPUT_PATH = os.path.join("..", "test_cases", "generated_tests.json")
PLAYWRIGHT_SCRIPT_PATH = os.path.join("..", "playwright_tests", "tests", "recruter_ai.spec.ts")

def clean_and_load_json(file_path):
    """
    Reads a file, automatically cleans it of markdown code blocks,
    and then loads it as JSON.
    """
    print(f"Reading and cleaning JSON file from: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_content, re.DOTALL)
        
        json_string = ""
        if match:
            print("✅ Found JSON inside a markdown block. Extracting it.")
            json_string = match.group(1)
        else:
            print("No markdown block found. Treating file as plain JSON.")
            json_string = raw_content

        return json.loads(json_string)

    except Exception as e:
        print(f"❌ Error reading, cleaning, or parsing {file_path}: {e}")
        return None

def convert_json_to_playwright():
    """Reads cleaned JSON and generates a syntactically correct Playwright script."""
    
    data = clean_and_load_json(JSON_INPUT_PATH)
    if not data:
        return

    # Use a list to build the lines of the script
    script_lines = [
        "import { test, expect } from '@playwright/test';",
        "",
        "test.describe('QAgenie Tests for Recruter.ai', () => {"
    ]

    for tc in data.get('test_cases', []):
        test_title = tc.get('title', 'Untitled Test').replace("'", "\\'")
        test_id = tc.get('id', 'N/A')

        script_lines.append(f"  test('{test_id}: {test_title}', async ({{ page }}) => {{")
        
        description = tc.get('description', 'No description provided.').replace('\\n', ' ').replace('\n', ' ')
        script_lines.append(f"    // Description: {description}")

        for step in tc.get('steps', []):
            action = step.get('action', '').lower()
            selector = step.get('selector', '')
            
            # Use double quotes for locators to avoid conflicts with single quotes inside
            safe_selector = selector.replace('"', '\\"')

            line = "    " # Start with standard indentation
            if action in ['visit', 'navigate']:
                value = step.get('value', 'https://www.recruter.ai/').replace('[your-application-url]', 'https://www.recruter.ai/')
                line += f"await page.goto('{value}');"
            elif action == 'click':
                line += f'await page.locator("{safe_selector}").click();'
            elif action in ['input', 'fill']:
                value = step.get('value', '').replace("'", "\\'")
                line += f'await page.locator("{safe_selector}").fill(\'{value}\');'
            elif action == 'press':
                value = step.get('value', 'Enter')
                line += f'await page.locator("{safe_selector}").press(\'{value}\');'
            elif action == 'upload_file':
                path = step.get('path', 'tests/fixtures/sample-resume.pdf').replace("\\", "/")
                line += f'await page.locator("{safe_selector}").setInputFiles(\'{path}\');'
            elif action in ['expectvisible', 'assertvisible', 'verify_element_is_visible']:
                line += f'await expect(page.locator("{safe_selector}")).toBeVisible();'
            else:
                line += f"// Skipping unknown action: {action}"

            script_lines.append(line)
        
        # Add a delay for demo purposes
        script_lines.append("    await page.waitForTimeout(500);")
        script_lines.append("  });")
        script_lines.append("") # Add a blank line between tests

    script_lines.append("});")

    # Join all lines with a proper newline character
    final_script = "\n".join(script_lines)

    os.makedirs(os.path.dirname(PLAYWRIGHT_SCRIPT_PATH), exist_ok=True)
    with open(PLAYWRIGHT_SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(final_script)

    print(f"✅ Playwright script successfully regenerated at: {PLAYWRIGHT_SCRIPT_PATH}")


if __name__ == "__main__":
    convert_json_to_playwright()