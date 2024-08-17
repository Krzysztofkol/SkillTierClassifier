TIERS = ['E', 'D', 'C', 'B', 'A', 'S']

QUESTIONS = {
    'E': [
        "Do you have basic theoretical knowledge about this skill? (e.g., key terms, fundamental concepts)",
        "Can you perform simple, guided tasks related to this skill with assistance?",
        "Are you able to understand and follow basic instructions or tutorials for this skill?"
    ],
    'D': [
        "Can you perform simple tasks related to this skill independently, without guidance?",
        "Do you understand the basic principles behind the skill well enough to explain them to a beginner?",
        "Are you able to recognize common mistakes or pitfalls related to this skill, even if you might still make them yourself?",
        "Can you use basic tools or techniques associated with this skill without constant reference to guides?"
    ],
    'C': [
        "Can you complete routine tasks efficiently and with minimal guidance?",
        "Are you able to troubleshoot and solve common problems related to this skill?",
        "Can you adapt your knowledge to slightly unfamiliar situations within this skill area?",
        "Do you understand best practices for this skill and apply them consistently in your work?",
        "Are you able to plan and execute small projects or tasks using this skill with minimal supervision?"
    ],
    'B': [
        "Are you comfortable with most aspects of the skill, including some advanced concepts?",
        "Can you work independently on complex tasks or projects related to this skill?",
        "Are you able to critically evaluate different approaches or solutions within this skill area?",
        "Can you effectively explain complex aspects of this skill to others who are less proficient?",
        "Do you regularly seek out new information or techniques to improve your proficiency in this skill?"
    ],
    'A': [
        "Can you handle difficult, multifaceted tasks or projects using this skill with ease?",
        "Are you able to innovate and develop new approaches or solutions within this skill area?",
        "Can you mentor others effectively, helping them improve their proficiency in this skill?",
        "Are you recognized within your immediate professional circle as someone with high expertise in this skill?",
        "Can you synthesize information from various sources to gain deeper insights into complex problems related to this skill?"
    ],
    'S': [
        "Are you widely recognized as an expert in this skill, possibly beyond your immediate professional circle?",
        "Can you push the boundaries of current knowledge or practice in this skill area?",
        "Are you able to handle novel, extremely complex challenges that others in the field struggle with?",
        "Have you made original contributions to the theory or practice of this skill (e.g., publications, innovations, significant improvements to processes)?",
        "Can you accurately predict trends or future developments in this skill area based on your deep understanding?"
    ]
}

def get_next_question(tier, question_index=0):
    if tier not in TIERS or question_index >= len(QUESTIONS[tier]):
        return None
    return QUESTIONS[tier][question_index]

def get_next_tier(current_tier):
    current_index = TIERS.index(current_tier)
    if current_index < len(TIERS) - 1:
        return TIERS[current_index + 1]
    return None