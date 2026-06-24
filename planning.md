# TakeMeter Planning

## Project Topic

This project will build a text classifier for public AI Security Engineering discourse. The classifier will sort posts and comments into learning-focused technical categories based on whether the text explains a concept, discusses a tool or control, describes an attack or testing tactic, or provides low-signal/general commentary.

## Community Choice

I chose public Reddit discussions related to AI Security Engineering, LLM security, cybersecurity, machine learning, AI red teaming, prompt injection, RAG security, and secure AI deployment.

Potential sources include:

* r/cybersecurity
* r/LocalLLaMA
* r/aisecurity
* r/cybersecurityai
* r/MachineLearning
* r/netsec
* r/devsecops
* r/AskNetsec

This community is a good fit because public discussions about AI security contain a mix of definitions, tools, tactics, mitigations, opinions, and low-signal comments. That variety gives the classifier meaningful distinctions to learn.

## Label Taxonomy

### 1. concept_definition

This label is used for posts or comments that define, explain, or clarify an AI security engineering term, concept, risk, model behavior, system design issue, or architecture pattern.

Example:
Prompt injection happens when untrusted text causes a model or AI system to follow attacker-controlled instructions instead of the intended developer or system instructions.

### 2. tool_or_control

This label is used for posts or comments that discuss a specific tool, framework, benchmark, mitigation, guardrail, policy, or security control.

Example:
Garak and PyRIT can be used to automate LLM red-team testing and evaluate model behavior against prompt injection, jailbreak, and misuse scenarios.

### 3. attack_or_testing_tactic

This label is used for posts or comments that describe a specific attack technique, red-team method, testing tactic, exploit pattern, adversarial behavior, or abuse scenario.

Example:
An attacker can hide malicious instructions inside retrieved documents so a RAG system treats those instructions as trusted context during generation.

### 4. low_signal_or_general

This label is used for posts or comments that are too vague, broad, speculative, opinion-based, career-focused, hype-driven, dismissive, or off-topic to teach a concrete AI security concept, tool, control, or tactic.

Example:
AI security is going to be huge, and everyone should start learning it now.

## Edge Case Rules

If a comment fits more than one label, I will choose the most specific technical function it performs.

Priority order:

1. attack_or_testing_tactic
2. tool_or_control
3. concept_definition
4. low_signal_or_general

For example, if a comment says, “Use Garak to test whether your LLM is vulnerable to prompt injection,” it mentions a tool and a concept, but the main purpose is testing. I would label it `attack_or_testing_tactic`.

## Data Collection Plan

I will collect at least 200 public posts or comments from Reddit discussions related to AI Security Engineering. I will not use private Discord servers, private forums, private messages, or non-public content.

The dataset will be saved as a CSV with at least these columns:

* `text`
* `label`
* `source`
* `notes`

I will aim for a balanced label distribution so that no single label dominates the dataset. My target is approximately 50 examples per label.

## Hard Cases

A hard case may occur when a post both explains a concept and mentions a tool. For example, a comment may explain prompt injection while also recommending a scanner or guardrail. In that case, I will label based on the main purpose of the text.

Another hard case may occur when a comment is technically related to AI security but too vague to teach anything specific. If the text does not explain a concrete concept, tool, control, attack, or testing method, I will label it `low_signal_or_general`.

## Evaluation Plan

I will evaluate the fine-tuned model against a zero-shot Groq baseline. I will compare overall accuracy, per-class precision, recall, F1 score, and the confusion matrix.

Accuracy alone is not enough because the model could perform well overall while still failing on one important label. The confusion matrix will help show which labels the model confuses most often.

## Definition of Success

A successful model should perform better than the zero-shot baseline or reveal useful failure patterns. I will consider the project successful if the fine-tuned model improves over the baseline or if the evaluation clearly shows where the label taxonomy, dataset, or model struggled.

## Success Threshold

My target success threshold is:

- Fine-tuned DistilBERT accuracy of at least 70% on the held-out test set, or
- Fine-tuned DistilBERT performance within 10 percentage points of the Groq baseline.

If the fine-tuned model does not meet this threshold, I will still consider the project useful if the evaluation clearly identifies failure patterns through per-class metrics, wrong predictions, and the confusion matrix.

The reason for this threshold is that a classifier used in a real workflow should perform meaningfully better than random guessing and should be close enough to a strong baseline to justify using a smaller fine-tuned model.

## AI Tool Usage Plan

I may use AI tools to help stress-test label definitions, identify ambiguous examples, and summarize model failure patterns. I will not use AI to replace my own labeling judgment. Any AI-assisted labeling will be reviewed manually before being included in the final dataset.
