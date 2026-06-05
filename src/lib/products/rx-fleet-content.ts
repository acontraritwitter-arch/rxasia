export const rxFleetPage = {
  meta: {
    title: "RX Fleet",
    description:
      "Unified AI-powered platform for automated control of open-pit mining equipment — dispatching, telemetry, and high-precision positioning in one system.",
  },
  hero: {
    eyebrow: "RX Fleet",
    title: "Automatic dispatching & optimization for open-pit mining",
  },
  overview: {
    eyebrow: "PLATFORM ARCHITECTURE",
    lead: "RX Fleet is a unified AI-powered platform for automated control of all open-pit mining equipment.",
    body: "RX Fleet delivers real-time fleet optimization, intelligent dispatching, and high-precision positioning to maximize productivity and reduce operating costs — in a single AI-powered platform.",
  },
  provenResults: {
    eyebrow: "PROVEN RESULTS",
    items: [
      { value: "14%", label: "Increase in mining site productivity (up to)" },
      { value: "9%", label: "Fuel economy" },
      { value: "20%", label: "Extended frame & suspension life (haul truck advisor)" },
    ],
  },
  modules: [
    {
      id: "dispatching",
      eyebrow: "MODULE 01 — DISPATCHING & OPTIMIZATION",
      title: "AI-Driven Fleet Control",
      functionality:
        "Dynamic truck distribution along routes, shift scheduling using static and dynamic optimization, and an AI/ML recommendation engine that surfaces corrective actions.",
      featureEyebrow: "Functionality",
      features: [
        "Improved equipment performance and utilization rate",
        "Reduced fuel consumption",
        "Increased tire mileage",
        "Reduced maintenance and repair costs",
      ],
      metricsEyebrow: "Proven Efficacy",
      metrics: [
        { value: "14%", label: "Increase in mining site productivity" },
        { value: "9%", label: "Fuel economy" },
      ],
    },
    {
      id: "advisor",
      eyebrow: "HAUL TRUCK DRIVER ADVISOR",
      title: "Recommendation System",
      functionality:
        "The in-cab advisor guides every haul truck driver in real time — reducing fuel use, extending structural life, and improving fleet throughput without manual dispatcher intervention.",
      featureEyebrow: "Proven Effectiveness",
      features: [
        "Extended frame & suspension life",
        "Reduced fuel consumption",
        "Increased equipment availability",
      ],
      metrics: [
        { value: "20%", label: "Extended frame & suspension life" },
        { value: "5%", label: "Reduced fuel consumption" },
        { value: "6%", label: "Increased equipment availability" },
      ],
    },
    {
      id: "monitoring",
      eyebrow: "MODULE 02 — REMOTE EQUIPMENT MONITORING",
      title: "Diagnostics & Telemetry",
      functionality:
        "Full telemetry collection, operator compliance analytics, oil analysis for predictive maintenance, and automated OEE calculation for stationary and mobile equipment.",
      featureEyebrow: "Key Advantages",
      features: [
        "Generation of automated factor analysis of causes of technological and emergency equipment downtime",
        "Collection of baseline indicators for calculating the maintenance work cycle",
        "Automated calculation of OEE for both stationary and mobile equipment",
        "Extension of the maintenance cycle and increased service life before overhaul",
      ],
      metricsEyebrow: "Business Effects",
      metrics: [
        { value: "5%", label: "Increased equipment availability & longer MTBF" },
        { value: "2%", label: "Increased productivity" },
        { value: "3%", label: "Reduced maintenance costs" },
      ],
    },
    {
      id: "positioning",
      eyebrow: "MODULE 03 — HIGH-PRECISION SOLUTIONS",
      title: "Positioning & Guidance",
      functionality:
        "High-precision positioning and guidance for drilling and blasting workflows across the open-pit cycle.",
      featureEyebrow: "Capabilities",
      features: [
        "Increased productivity of drilling equipment by 4–10%",
        "Control and accounting of work and equipment downtime",
        "Improved quality of drilling and blasting operations",
        "Reduction of surveying work on surveying and marking",
        "Increasing the service life of drilling tools; reducing explosive consumption",
      ],
      metricsEyebrow: "Proven Results",
      metrics: [
        { value: "10%", label: "Improved equipment performance" },
        { value: "30%", label: "Reduction in surveying work" },
        { value: "6%", label: "Reduced explosive consumption" },
      ],
    },
  ],
  deployment: {
    eyebrow: "MODULAR DEPLOYMENT",
    title: "Start Small, Scale Without Limits",
    body: "RX Fleet is available in three deployment tiers. Each level builds on the previous, allowing mining operations to expand capabilities with no disruption.",
    tiers: [
      {
        name: "Dispatching & optimization",
        description: "Core AI-driven fleet control, routing, and shift optimization.",
      },
      {
        name: "Remote equipment monitoring",
        description: "Adds telemetry, OEE, predictive maintenance, and compliance analytics.",
      },
      {
        name: "High-precision solutions",
        description: "Full positioning and guidance for drilling, blasting, and surveying efficiency.",
      },
    ],
  },
  cta: {
    title: "Ready to see the difference?",
    body: "Schedule an intro session with our experts to walk you through the core modules and how they work together.",
    button: "Request Intro Session",
    href: "#contact",
  },
} as const;
