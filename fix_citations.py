with open('final_report.tex', 'r') as f:
    text = f.read()

replacements = {
    'kim2023ecmp': 'pei2024enabling',
    'patel2022reward': 'noaeen2022reinforcement',
    'nguyen2026deep': 'alavizadeh2022deep',
    'li2024ppo': 'matsuo2022deep',
    'wang2024saturation': 'pei2024enabling',
    'garcia2023discrete': 'alavizadeh2022deep',
    'zhang2025zero': 'matsuo2022deep'
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open('final_report.tex', 'w') as f:
    f.write(text)
