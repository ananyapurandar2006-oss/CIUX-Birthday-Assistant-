CIUX Birthday Assistant – Testing Documentation

University: GM University
Department: Computer Science and Engineering
Course: UE24CS3540 – Conversational Interfaces and UX
Project: CIUX Birthday Assistant
Version: V1 to V5
Dataset: 100 fictional people
Backend: Python Flask
Frontend: HTML, CSS and JavaScript

1. Testing Objective

The objective of testing is to verify that the Birthday Assistant understands natural-language questions, identifies user intent, extracts entities, maintains conversation context, retrieves accurate information from the dataset and supports voice interaction.

Testing also verifies that the assistant provides visible text responses when speech output is disabled.

2. Testing Categories

A total of 40 test utterances are prepared in four categories:

10 Direct questions

10 Paraphrased questions

10 Contextual and multi-turn questions

10 Ambiguous or unsupported questions

3. Test Cases

Category A: Direct Questions

No.

Test utterance

Expected behaviour

Observed result

1

Any nephew birthdays in September?

Return matching nephew birthdays

Passed

2

What are the upcoming birthdays?

Display upcoming birthdays

Pending

3

How many birthdays are there next month?

Return the birthday count

Pending

4

Is there any birthday tomorrow?

Display matching birthdays or no-result message

No matching people found

5

When is Nikhil Hegde's birthday?

Return Nikhil's birthday

Passed – 03 October 2001

6

Where does Rahul Patil stay?

Return Rahul's place

Passed – Bengaluru

7

When is Rahul Patil's birthday?

Return Rahul's birthday

Passed – 18 September 2004

8

When is my wife's birthday?

Return matching birthday information

Pending

9

Any birthdays in October?

Return matching October birthdays

Pending

10

How many nephews have birthdays in September?

Return the matching count

Pending

Category B: Paraphrased Questions

No.

Test utterance

Expected behaviour

Observed result

11

Do any of my nephews celebrate birthdays in September?

Return matching nephew birthdays

Pending

12

Tell me the birthdays coming soon

Display upcoming birthdays

Pending

13

Is anyone's birthday tomorrow?

Return matching records or no-result message

Pending

14

Can you find Nikhil Hegde's date of birth?

Return Nikhil's date of birth

Pending

15

Which city does Rahul Patil live in?

Return Rahul's place

Pending

16

Give me the birthday count for next month

Return the correct count

Pending

17

Show September birthdays of my nephews

Return matching nephew birthdays

Pending

18

Whose birthday is in October?

Return October birthday records

Pending

19

Find the birthday details of Rahul Patil

Return Rahul's birthday

Pending

20

Are there any upcoming celebrations?

Display upcoming birthdays

Pending

Category C: Contextual and Multi-Turn Questions

No.

Conversation

Expected behaviour

Observed result

21

Any nephew birthdays in September? → What about October?

Remember nephew relationship and change month

Passed – Nikhil Hegde, 03 October

22

Ask about September → What about November?

Remember previous relationship and update month

Pending

23

Ask about October → Which one comes first?

Use previous results to identify the earliest

Pending

24

When is my nephew's birthday? → Nikhil

Resolve the selected person

Pending

25

Ask about Rahul's birthday → Where does he stay?

Remember Rahul and return his place

Pending

26

Ask about upcoming birthdays → What about next month?

Interpret the follow-up month

Pending

27

Ask about nephews → What about nieces?

Update the relationship

Pending

28

Ask about September → What about October birthdays?

Update the month

Pending

29

Ask about Nikhil → Where does he stay?

Remember the selected person

Pending

30

Ask about October → How many are there?

Count matching October records using context

Pending

Category D: Ambiguous or Unsupported Questions

No.

Test utterance

Expected behaviour

Observed result

31

When is my nephew's birthday?

Ask which nephew the user means

Pending

32

Tell me about his birthday

Ask for clarification if person is unknown

Pending

33

Who is the kindest person?

State that the dataset does not support this

Pending

34

Any birthdays on 31 February?

Reject the invalid date and avoid inventing a result

Pending

35

Where does an unknown person stay?

Handle missing person information

Pending

36

Tell me something about everyone

Handle unsupported broad request

Pending

37

Who has the most beautiful birthday?

Avoid fabricating information

Pending

38

What is my friend's phone number?

State that this information is unavailable

Pending

39

Find a birthday for an unknown name

Handle unknown person correctly

Pending

40

Tell me the birthday of someone I have not mentioned

Ask for a person's name

Pending

4. Voice Interface Testing – V5

No.

Feature tested

Observed result

1

Microphone input

Passed

2

Recognition of birthday question

Passed

3

Recognition of relationship term – Nephew

Passed

4

Recognition of month – September

Passed

5

Voice follow-up – What about October?

Passed

6

Person name recognition – Nikhil Hegde

Recognized with transcript variation

7

Indian place name – Rahul Patil / Bengaluru

Recognized with transcript variation

8

Birthday date lookup

Passed

9

Speech output

Passed

10

Text-only mode

Passed

5. Testing Observations

The voice interface successfully captures spoken questions using browser speech recognition.

Recognized speech is placed in the same question input field.

The assistant processes voice questions through the existing Flask backend.

The assistant identifies intent and extracts entities such as month and relationship.

Dialogue context is retained during follow-up questions.

Birthday and location information is retrieved from the structured dataset.

Speech-recognition mistakes can occur with names and Indian place names.

Text responses remain available even when speech output is disabled.

6. Error Analysis

Speech recognition and Natural Language Understanding are separate stages.

ASR error: The browser may recognize a person's name incorrectly.

NLU error: The system may identify the wrong intent or entity.

Dialogue error: The system may incorrectly reuse previous context.

Database error: The query may return incorrect or missing records.

Response error: The correct result may be presented incorrectly.

Testing should identify which layer caused an error before changing the code.

7. Evaluation Metrics

The following metrics are considered for evaluating the system:

Intent Accuracy: Correctly identified intents.

Entity Accuracy: Correctly extracted names, dates, months and relationships.

Task Success: Questions answered with the correct dataset information.

Clarification Success: Ability to ask useful clarification questions.

Grounded Factuality: Accuracy of birthday, place and relationship information.

Latency: Time taken to display an answer.

Voice Recognition Success: Accuracy of speech transcription.

User Experience: Ease of interaction and clarity of responses.

8. Privacy and Data Protection

The project uses a synthetic dataset containing fictional people. Real personal information should not be uploaded or exposed publicly.

API keys and environment variables should remain private and must not be committed to a public repository.

9. Conclusion

The CIUX Birthday Assistant demonstrates the development of a conversational interface through five versions, progressing from rule-based processing to intent and entity extraction, dialogue management, grounded language understanding and voice interaction.

The V5 implementation supports microphone input, speech recognition, speech synthesis and text-based responses while preserving the existing backend.

Testing demonstrates successful voice queries, contextual follow-ups, person lookup and place lookup. Additional test cases are included to evaluate the reliability, accuracy and usability of the system.

The project demonstrates how voice can act as an additional interaction channel while the structured dataset remains the source of factual information.
