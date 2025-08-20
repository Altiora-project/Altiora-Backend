import json

with open(
    "fixtures/create_fixtures/text_privace_policy.txt", "r", encoding="utf-8"
) as f:
    policy_text = f.read().strip()
with open(
    "fixtures/create_fixtures/text_processing_of_personal_data.txt",
    "r",
    encoding="utf-8",
) as f:
    consent_text = f.read().strip()
fixture = [
    {
        "model": "api.policy",
        "pk": 1,
        "fields": {
            "title": "Политика конфиденциальности",
            "slug": "privacy_policy",
            "text": policy_text,
        },
    },
    {
        "model": "api.policy",
        "pk": 2,
        "fields": {
            "title": "Согласие на обработку персональных данных",
            "slug": "consent_to_the_processing_of_personal_data",
            "text": consent_text,
        },
    },
]
with open("fixtures/policy.json", "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=4)

print("Фикстура сохранена в fixtures/policy.json")
