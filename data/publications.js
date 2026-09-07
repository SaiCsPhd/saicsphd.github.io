export const publications = [
  {
    title: 'IndicSafeEval: Safety Robustness of Large Language Models under Multilingual Persuasive Jailbreak Attacks',
    venue: 'EMNLP 2026',
    venueFullName: 'The 2026 Conference on Empirical Methods in Natural Language Processing',
    year: '2026',

    description:
      '<strong>IndicSafeEval</strong> evaluates how well LLMs resist persuasive jailbreak attacks in four Indian languages—Bengali, Hindi, Marathi, and Punjabi. It tests five open-source models using 7,200 adversarial prompts across 10 harmful-content categories and six persuasion strategies, including logical appeal, authority endorsement, anchoring, priming, misrepresentation, and confirmation bias. The study finds that safety robustness varies substantially by language, persuasion style, and harm category.',

    tags: [
      'Multilingual LLM safety',
      'Indic languages',
      'Persuasive jailbreaks',
      'Jailbreak robustness',
      'Safety alignment',
    ],

    links: [
      { label: 'Paper', url: 'https://arxiv.org/pdf/2609.03781v2' },
      { label: 'Code', url: 'https://github.com/MonSaikat/IndicSafeEval' },
    ],
  },

  {
    title: 'Multi-Channel Stacked TextCNN for Biomedical Multilabel Classification',
    venue: 'FOSS-CILT 2024',
    venueFullName:
      'International Conference on FOSS Approaches towards Computational Intelligence and Language Technology',
    year: '2024',

    description:
      'Proposed <strong>MCSTCNN</strong> (Multi-Channel Stacked TextCNN), a novel deep learning architecture for multilabel text classification in the biomedical domain. The model leverages multi-channel convolutional feature extraction stacked across hierarchical levels to capture fine-grained semantic patterns in clinical and scientific literature.',

    tags: [
      'Multilabel Classification',
      'Biomedical Text Mining',
      'TextCNN',
      'Deep Learning',
    ],

    // Uncomment when you have the actual paper/code links
    // links: [
    //   { label: 'Paper', url: 'https://...' },
    //   { label: 'Code', url: 'https://...' },
    // ],
  },
];
