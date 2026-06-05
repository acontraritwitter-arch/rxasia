"use client";

import { motion, useInView } from "framer-motion";
import { useRef, ReactNode } from "react";

interface RevealProps {
  children: ReactNode;
  delay?: number;
  direction?: "up" | "down" | "left" | "right";
  blur?: boolean;
  className?: string; // Добавили поддержку классов
}

export function Reveal({ 
  children, 
  delay = 0, 
  direction = "up",
  blur = true,
  className = "w-full" // По умолчанию заставляем обертку тянуться на всю ширину
}: RevealProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-10%" });

  const yOffset = direction === "up" ? 20 : direction === "down" ? -20 : 0;
  const xOffset = direction === "left" ? 20 : direction === "right" ? -20 : 0;

  return (
    <motion.div
      ref={ref}
      className={className}
      initial={{ 
        opacity: 0, 
        y: yOffset, 
        x: xOffset,
        filter: blur ? "blur(8px)" : "blur(0px)" 
      }}
      animate={isInView ? { 
        opacity: 1, 
        y: 0, 
        x: 0,
        filter: "blur(0px)" 
      } : {}}
      transition={{
        duration: 0.8,
        delay: delay,
        ease: [0.21, 0.47, 0.32, 0.98],
      }}
    >
      {children}
    </motion.div>
  );
}