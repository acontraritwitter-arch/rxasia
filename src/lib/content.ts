export const site = {
  name: "RXAsia",
  tagline: "Your trusted partners in digital future",
  heroTitle: "Empowering business with tech excellence",
  contactEmail: "info@rxasia.kz",
  address: "Kazakhstan, Almaty, 69 Tole bi street, apartment 9, 050026",
} as const;

export const navLinks = [
  { label: "ABOUT", href: "#about" },
  { label: "SERVICES", href: "#services" },
  { label: "INDUSTRIES", href: "#industries" },
  { label: "APPROACH", href: "#approach" },
  { label: "CAREERS", href: "#careers" },
] as const;

export const stats = [
  { value: "300", label: "Customers across the globe" },
  {
    value: "32",
    label: "Years of experience — shaping the Web 1.0 through 3.0+",
  },
  { value: "500", label: "Talents working with passion and zest" },
  { value: "900", label: "Delivered mission critical projects with honor" },
] as const;

export const achievements = [
  {
    title: "Extend your team",
    body: [
      "Boost your dev capabilities with RXAsia's talent.",
      "Our dedicated specialists will handle your tasks to your schedule.",
      "We'll take care of hiring, office expenses, and rotation of workforce.",
    ],
    cta: "Contact us",
  },
  {
    title: "Delegate your idea",
    body: [
      "Support your operations with a custom-built application.",
      "We'll dive deep into your business context and propose a set of solutions.",
      "We'll handle development and integrations — for you to focus on the essentials.",
    ],
    cta: "Contact us",
  },
] as const;

export const consulting = {
  title: "IT & Digital Transformation Consulting",
  body: "We discover new digital opportunities to bring out the best of the work automation — to exceed strategic requirements of your company and to overachieve business goals. We focus on empowerment of your customers and employees and keep in mind that technology is here to alleviate our challenges — not multiply them.",
} as const;

export const services = {
  intro:
    "We create, find and integrate platforms, applications, and services with the end goal of sustainable improvement of your operations — or bringing them up to another level. Our solutions are scalable, masterful and elegant — just as you like.",
  items: [
    {
      title: "Digital Design & Development",
      description:
        "Our 30+ years of various industrial experience have led us to believe that software development can be actually streamlined. We combined our enterprise project management best practices and methodology and developed a set of tools that allow us and our customers to achieve high transparency, predictability and operational excellence of software production — which can be critical in tight competition. We are happy to share these findings with you — it's not a secret.",
    },
    {
      title: "Digital Factory Framework",
      description:
        "We hire, train and onboard specialized expert groups to meet your requirements and practices. If necessary, we collaborate with outsourcing employees — whose qualification is our responsibility.",
    },
    {
      title: "Dedicated Development",
      description: "",
    },
  ],
} as const;

export const industryItems = [
  { slug: "banking", name: "Banking" },
  { slug: "logistics", name: "Logistics" },
  { slug: "airports", name: "Airports" },
  { slug: "retail", name: "Retail" },
  { slug: "mining", name: "Mining" },
] as const;

/** @deprecated Use `industryItems` */
export const industries = industryItems.map((item) => item.name);

export const approachItems = [
  {
    index: 1,
    title: "Fundamental analysis",
    description:
      "We research your company eco-system to integrate software and define the optimization vectors. Visual concepts, prototypes and simplified solutions get the maximum possible output from the resources invested in the market testing.",
  },
  {
    index: 2,
    title: "Picking the right toolset",
    description:
      "We quickly deploy for your project, choosing a practical and cost-effective solution. Then we build on your business metrics. We are ready to offer our clients a choice of a platform, self-developed and individually tailored solutions.",
  },
  {
    index: 3,
    title: "Transparent collaboration",
    description:
      "Professional wisdom, constant communication and use of optimal infrasctucture will get our work streamlined. Our advanced tools help to meet the customer\u2019s requirements and act according to the changing demands and conditions of the market.",
  },
  {
    index: 4,
    title: "Digital strategy",
    description:
      "We evaluate the market trends and leverage them for your growth vectors, using KPI-based approach to maintain the business's competitive ability in the future.",
  },
  {
    index: 5,
    title: "Flexibility and continuity",
    description:
      "We guarantee an accelerated start of the project and consistent integration, managed at the stage of exploitation.",
  },
  {
    index: 6,
    title: "Scalability",
    description:
      "Our technology and specialized scalable teams allow us to excercise precise expense control and adjust the strategy per your requirements.",
  },
] as const;

export const aboutBlocks = {
  whatWeDo: {
    eyebrow: "WHAT WE DO",
    body: "We develop transformational technologies that assist our customers in redefining the future and achieving their competitive edge.",
  },
  mission: {
    eyebrow: "OUR MISSION",
    body: "We provide our profound cross-industry expertise and the best talent we can find for the market leaders that build a better future.",
  },
  achievementsEyebrow: "OUR ACHIEVEMENTS",
  servicesEyebrow: "OUR SERVICES",
  approachEyebrow: "OUR APPROACH",
  approachTagline: "Excellence in our DNA",
  industriesEyebrow: "INDUSTRIES",
} as const;
