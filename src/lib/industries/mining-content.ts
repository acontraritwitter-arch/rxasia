export const miningPage = {
  meta: {
    title: "Mining",
    description:
      "Solutions that bring clarity to mining operations. Domain expertise, structured implementation, and measurable outcomes for mining companies.",
  },
  hero: {
    eyebrow: "Mining",
    title: "Solutions that bring clarity to mining operations",
  },
  whatWeDo: {
    eyebrow: "WHAT WE DO",
    body: "By combining domain knowledge with technical capabilities, we help mining companies improve processes, enhance safety, and achieve more predictable outcomes. Our solutions are developed for real operating conditions and tested through practical implementation.",
  },
  advantages: {
    eyebrow: "OUR ADVANTAGES",
    title: "Why Partner With Us",
    items: [
      {
        index: 1,
        title: "Industry experience",
        body: "Our team includes engineers with background in mining operations. We understand the context in which you work and the metrics that matter to your business.",
      },
      {
        index: 2,
        title: "Structured implementation",
        body: "We follow established methodologies to maintain project timelines and budgets. Regular reporting and clear communication help ensure alignment throughout the engagement.",
      },
      {
        index: 3,
        title: "Focus on business outcomes",
        body: "Our solutions are designed with specific operational and financial objectives in mind. We work to deliver measurable improvements in productivity and cost efficiency.",
      },
      {
        index: 4,
        title: "Integrated approach",
        body: "We develop systems that connect with your existing infrastructure rather than creating isolated tools. This helps maintain data consistency and operational continuity.",
      },
      {
        index: 5,
        title: "Adaptability to local conditions",
        body: "Each site has its own characteristics. We take into account your equipment, environment, and operational practices when designing solutions.",
      },
      {
        index: 6,
        title: "Long-term perspective",
        body: "We aim to build relationships that extend beyond individual projects. Our interest is in supporting your ongoing development through reliable technology and sustained expertise.",
      },
    ],
  },
  solutions: {
    eyebrow: "OUR SOLUTIONS",
    items: [
      {
        name: "RX Belt",
        features: ["Ore contamination and fragmentation control", "Tears / defects detection"],
      },
      {
        name: "RX Fleet",
        href: "/rx-fleet",
        features: [
          "Open pit / UG control",
          "Dispatching logic",
          "High-precision navigation",
        ],
      },
      {
        name: "RX Efficiency",
        features: ["Flotation control", "Simple process cue"],
      },
      {
        name: "RX Robotics",
        features: ["Robotic ore breaker", "More robotic solutions"],
      },
    ],
  },
  caseStudies: {
    eyebrow: "CASE STUDIES",
    items: [
      {
        title: "Smart automation of sulfide flotation operations",
        body: "Autonomous flotation control system leveraging computer vision and machine learning to stabilize and optimize the process.",
      },
      {
        title: "Real-time control and optimization of converter blowing end point",
        body: "Determination of molten metal chemical composition based on off-gas spectrometry analysis to control iron oxidation and sulfur removal.",
      },
      {
        title: "Conveyor bulk product mass measurement",
        body: "Continuous monitoring of roller motion sensors to detect conveyor belt start and stop events.",
      },
    ],
  },
} as const;
