Excellent! Based on the VDJdb schema and your enhanced supervisor system, here are test questions organized by complexity and research type. These will help you validate the iterative research capabilities:

## 🔍 **Basic Database Exploration**
*Tests initial data_analyst routing and basic query generation*

1. **"What are the most common HLA alleles associated with SARS-CoV-2 epitopes in VDJdb?"**
   - *Expected flow*: data_analyst → biomedical_researcher (for clinical context) → reporter

2. **"Show me all TCR sequences that recognize the SARS-CoV-2 spike protein epitope YLQPRTFLL"**
   - *Expected flow*: data_analyst → biomedical_researcher (epitope significance) → potential follow-up

3. **"What CDR3 motifs are most frequently found in TCRs targeting influenza antigens?"**
   - *Expected flow*: data_analyst → coder (pattern analysis) → biomedical_researcher → reporter

## 🧬 **Pattern Discovery & Follow-up**
*Tests the supervisor's ability to detect interesting findings and trigger deeper research*

4. **"Find TCR sequences with unusually high VDJdb confidence scores and investigate what makes them special"**
   - *Expected flow*: data_analyst → biomedical_researcher (literature on high-confidence TCRs) → data_analyst (follow-up patterns) → reporter

5. **"Identify TCR chains that use the same V-segment but recognize different viral epitopes"**
   - *Expected flow*: data_analyst → biomedical_researcher (cross-reactivity research) → data_analyst (validation) → coder (statistical analysis)

6. **"Are there any TCR sequences in VDJdb that appear to recognize multiple different epitopes?"**
   - *Expected flow*: data_analyst → biomedical_researcher (polyspecificity literature) → data_analyst (deeper analysis)

## 🔬 **Cross-Validation Research**
*Tests database-literature integration loops*

7. **"What does VDJdb tell us about TCR responses to CMV, and how does this compare to recent literature?"**
   - *Expected flow*: data_analyst → biomedical_researcher → data_analyst (follow-up based on literature) → reporter

8. **"Find HLA-B*07:02 restricted TCRs in VDJdb and validate their clinical relevance"**
   - *Expected flow*: data_analyst → biomedical_researcher (HLA-B*07:02 associations) → data_analyst (specific epitope analysis)

9. **"Investigate whether the TCR repertoire patterns for cancer antigens in VDJdb match what we know from immunotherapy studies"**
   - *Expected flow*: data_analyst → biomedical_researcher → data_analyst (refinement) → biomedical_researcher (clinical trials)

## 🧮 **Computational Analysis**
*Tests integration with coder agent for statistical analysis*

10. **"Analyze the diversity of CDR3 lengths for different antigen species and calculate statistical significance"**
    - *Expected flow*: data_analyst → coder (statistical analysis) → biomedical_researcher (biological significance) → reporter

11. **"Create a visualization showing the relationship between VDJdb confidence scores and V-segment usage patterns"**
    - *Expected flow*: data_analyst → coder (visualization) → biomedical_researcher (interpretation) → reporter

12. **"Calculate the Shannon diversity index for TCR repertoires targeting different viral families"**
    - *Expected flow*: data_analyst → coder (diversity calculation) → biomedical_researcher (immunological context)

## 🦠 **Disease-Specific Deep Dives**
*Tests sustained iterative research on focused topics*

13. **"Comprehensively analyze all COVID-19 related TCR data in VDJdb - what can we learn about protective immunity?"**
    - *Expected flow*: Multiple rounds of data_analyst → biomedical_researcher → data_analyst (follow-ups) → coder (analysis) → reporter

14. **"Investigate TCR responses to tumor antigens - what patterns exist and what do they suggest for immunotherapy?"**
    - *Expected flow*: data_analyst → biomedical_researcher → data_analyst (refined queries) → biomedical_researcher (clinical implications)

15. **"Compare TCR repertoires between viral and bacterial antigens - are there fundamental differences?"**
    - *Expected flow*: data_analyst → biomedical_researcher → data_analyst (comparative analysis) → coder (statistics) → biomedical_researcher

## 🔄 **Multi-Hypothesis Testing**
*Tests the supervisor's ability to pursue multiple research threads*

16. **"I suspect that certain CDR3 motifs might be associated with cross-reactive TCRs. Investigate this hypothesis using VDJdb data."**
    - *Expected flow*: data_analyst → coder (motif analysis) → biomedical_researcher (cross-reactivity literature) → data_analyst (validation)

17. **"Test whether TCRs with longer CDR3 sequences tend to target more complex epitopes"**
    - *Expected flow*: data_analyst → coder (correlation analysis) → biomedical_researcher (structural studies) → reporter

18. **"Explore whether the method used to identify TCRs (tetramer vs sequencing) affects the types of sequences found"**
    - *Expected flow*: data_analyst → biomedical_researcher (methodology papers) → data_analyst (method-stratified analysis) → coder

## 🎯 **Clinical Translation**
*Tests research with therapeutic implications*

19. **"Find the most promising TCR candidates for adoptive cell therapy based on VDJdb data and current clinical trials"**
    - *Expected flow*: data_analyst → biomedical_researcher (clinical trials) → data_analyst (candidate identification) → biomedical_researcher (validation)

20. **"Identify TCRs targeting shared tumor antigens that might be suitable for off-the-shelf TCR therapy"**
    - *Expected flow*: data_analyst → biomedical_researcher → data_analyst (safety analysis) → biomedical_researcher (clinical feasibility)

## 🧪 **Method Validation**
*Tests research quality and reproducibility*

21. **"How reliable are the different experimental methods used in VDJdb, and what does this mean for our analysis?"**
    - *Expected flow*: data_analyst → biomedical_researcher (method comparison studies) → coder (statistical analysis) → reporter

22. **"Investigate whether low VDJdb confidence scores correlate with specific experimental limitations"**
    - *Expected flow*: data_analyst → biomedical_researcher → data_analyst (method-score correlation) → biomedical_researcher

## 🌟 **Complex Integration Challenges**
*Tests the supervisor's most advanced capabilities*

23. **"Design a personalized TCR therapy approach: analyze HLA-A*02:01 restricted melanoma TCRs and evaluate their clinical potential"**
    - *Expected flow*: Multiple iterations of data_analyst ↔ biomedical_researcher ↔ coder with follow-up questions

24. **"Investigate the evolutionary basis of TCR cross-reactivity patterns found in VDJdb"**
    - *Expected flow*: data_analyst → biomedical_researcher → data_analyst → coder → biomedical_researcher (evolutionary studies)

25. **"Create a comprehensive research report on VDJdb's coverage of autoimmune disease TCRs and identify critical gaps for future research"**
    - *Expected flow*: Extended iterative cycle ending with comprehensive reporter synthesis

## 🎪 **Edge Cases & Error Handling**
*Tests supervisor robustness*

26. **"Find TCRs that recognize epitopes from extinct species"** *(Should find little/no data)*
27. **"Analyze TCR responses to epitopes longer than 20 amino acids"** *(Edge case analysis)*
28. **"What can VDJdb tell us about TCR responses in non-human species?"** *(Limited scope test)*

These questions range from simple (10-minute analysis) to complex (30+ minute iterative research) and will help you test:

- **Basic routing decisions**
- **Iterative deepening triggers** 
- **Cross-validation loops**
- **Multi-agent coordination**
- **Research completion criteria**
- **Domain expertise application**

Start with the simpler questions to validate basic functionality, then progress to the complex integration challenges to test the supervisor's full iterative research capabilities!