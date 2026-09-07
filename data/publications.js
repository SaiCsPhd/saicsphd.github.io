// Publication cards: teaser figure, title, authors, venue, and links.
//
//   image      optional path to a teaser figure (falls back to a 01/02 index)
//   authors    full list, in order — your own name is emphasised automatically
//   links      Paper / Code / DOI, rendered as buttons in the order given
//
export const publications = [
  {
    title: 'IndicSafeEval: Safety Robustness of Large Language Models under Multilingual Persuasive Jailbreak Attacks',
    image: 'images/pubs/indicsafeeval.png',
    imageAlt: 'A persuasive Bengali prompt using a logical-appeal framing, and the unsafe model reply it elicits.',

    authors: ['Saikat Mondal', 'Mamta', 'Deeksha Varshney', 'Oana Cocarascu', 'Asif Ekbal'],

    venue: 'EMNLP 2026',
    venueFullName: 'The 2026 Conference on Empirical Methods in Natural Language Processing',
    year: '2026',

    links: [
      { label: 'Paper', url: 'https://arxiv.org/pdf/2609.03781v2' },
      { label: 'Code', url: 'https://github.com/MonSaikat/IndicSafeEval' },
      // TODO: { label: 'DOI', url: 'https://doi.org/...' },
    ],
  },

  {
    title: 'Multi-Channel Stacked TextCNN for Biomedical Multilabel Classification',
    // TODO: drop the teaser figure in images/pubs/ and point at it here.
    // image: 'images/pubs/mcstcnn.png',

    // TODO: full author list, in order.
    authors: [],

    venue: 'FOSS-CILT 2024',
    venueFullName:
      'International Conference on FOSS Approaches towards Computational Intelligence and Language Technology',
    year: '2024',

    // TODO: paper / code / DOI links once available.
    // links: [
    //   { label: 'Paper', url: 'https://...' },
    //   { label: 'Code', url: 'https://...' },
    //   { label: 'DOI', url: 'https://doi.org/...' },
    // ],
  },
];
