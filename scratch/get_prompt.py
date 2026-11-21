import json

with open(r'C:\Users\akshi\.gemini\antigravity\brain\a312a4a0-484c-4563-abe7-cdb8eacdccca\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT' and 'MEDILINK ENTERPRISE v4.0' in data.get('content', ''):
            with open('scratch/v4_full_prompt.txt', 'w', encoding='utf-8') as out:
                out.write(data['content'])
            print("Extracted prompt! Length:", len(data['content']))
            break
