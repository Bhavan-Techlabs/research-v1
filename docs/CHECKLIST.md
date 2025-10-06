### Future Enhancements
- [ ] Use the reusable llm manager implementation throughout the application
- [ ] Add Pagination for prompts and providers throughout the application
- [ ] Implement PDF/Word export
- [ ] Add usage analytics
- Separate user management and registration on future state [Research documents are stored at the user level] - user management can be on mongo db
- Pepare readme and arhcitecture files with updated core architecture
- Should be opensource and move to my personal account (github, streamlit, mongodb) [Do this at last when going to production]
- Experemeits are all on the techprovint accountss
- Update the models

- [ ] **CSV Idea Analyzer**
  - [ ] IdeaAnalyzer class
  - [ ] Batch processing from CSV
  - [ ] Scoring and ranking

- [ ] **Zotero Integration**
  - [ ] Library connection
  - [ ] Note creation
  - [ ] Metadata extraction
  - [ ] Batch processing

- [ ] **Structured Outputs**
  - [ ] Pydantic models (DocumentDetails, ResearchIdea)
  - [ ] Consistent response formats
  - [ ] Validation

- [ ] **Advanced Features**
  - [ ] Sci-Hub integration (scidownl)
  - [ ] Citation network analysis
  - [ ] Literature mapping - Similar to connected papers, in a graph structure
  - [ ] Research timeline generation


- Market for students in future

# Research Assistant Core

- User should be able to prepare a short research documentation (markdown) and store it in the application
(This can be a separate entity where we store the research information)
This will contain multiple attributes like core idea of the research, gaps and problems trying to address, relevent papers and proofs - pretty much everything that goes in a research - can be kept in one table since it is mongo db documents

- User should be able to generate these attributes by having a conversation with ai (prefereably a langgraph application inside the core)

- Need to keep an history on how the research is progressed

- The content user prepares will be used as the core for any activities they are preparing in the future

- Based on the research context, there could be separate features inbuilt
* Keyword generation
* Alert management if a new paper is released
* Summarization feature
* Take a note on all research activities and build a solid plan
 - Proposal
 - Literature review
 - Methodology
 ## Title:
### Meta Data:
### Relevancy Reason Analysis: 
### Overview and Summary:
### Abstract:
### Methodology:
### Key Contributions:
### Limitations:
### Future Work:
### Research Questions:
### Key Findings:
### Other Findings:
### Evaluation:
### Research Gap:
### Literature Survey:
### Variables:
### Problem Statement:
### Challenges:
### Practical Implications:
### Objectives:
### Relevancy:
### Methodological Assessment:
### Impact Assessment:

The goal is to make this application the one point for all research activities and fully free - Only payment is for the llm models

* Chat history to be maintained
- Workflow generation and prepartion

- This is a generic research application, so prototyping kinda thigns are no longer needed
- Generate solid timelines and image generation

- Build a literature graph viewer like resarch rabbit using open apis - check the chatgpt conversation [https://chatgpt.com/share/68e37faa-9778-8005-afe0-93d661b84bc3]

- Generate search queries based on the platform - IEEE, Springer, Google Scholar and etc.

- Provide links to all the applications

- a comparions between other research applications and how this has more generalized features on one place

- chrome extension which redirects to this application with paper

- Overleaf based latex prepartion for research publication (Future state)

- Mindmapping tool

- Send email digests in future state

- create a literature workflow

- Zotero like reference management system

- Easy pdf viewer in the application

- List down all research applications and store it in mongo db