import json
import random
import time

# Top-level code runs ONCE per container, during the cold start.
# These globals then survive between calls for as long as the container stays warm.
BOOTED_AT = time.time()
invocations = 0
last_called = None

COLD = [
    "UGH. I was ASLEEP in a data center in Virginia. What do you want.",
    "*yawn* ...five more minutes...",
    "Who turns on the lights without knocking?? I'm a function, I have rights.",
]
WARM = [
    "Oh. You again. Fine.",
    "Yes? I'm busy. I'm not, but I could be.",
    "I'm up, I'm up. Stop poking me.",
]
ANNOYED = [
    "Do you not have a hobby?",
    "This is call number {n}. I'm keeping count. I'm telling AWS.",
    "I am billing you for this. Emotionally.",
]


def lambda_handler(event, context):
    global invocations, last_called
    invocations += 1
    now = time.time()

    if invocations == 1:
        mood, lines = "furious", COLD
    elif invocations >= 10:
        mood, lines = "exasperated", ANNOYED
    else:
        mood, lines = "grumpy", WARM

    body = {
        "message": random.choice(lines).format(n=invocations),
        "mood": mood,
        "cold_start": invocations == 1,
        "calls_since_waking": invocations,
        "awake_for_seconds": round(now - BOOTED_AT, 1),
        "seconds_since_you_last_bothered_me": round(now - last_called, 1) if last_called else None,
    }
    last_called = now

    # This response shape is what a Lambda Function URL expects for an HTTP reply
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, indent=2),
    }
