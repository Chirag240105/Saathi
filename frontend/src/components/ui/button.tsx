import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-control font-bold transition-colors disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-teal text-white hover:bg-teal-dark",
        outline: "border-2 border-teal bg-surface text-teal-dark hover:bg-teal-wash",
        ghost: "text-ink hover:bg-sand-deep",
        danger: "bg-coral-ink text-white hover:opacity-90",
      },
      size: {
        md: "min-h-tap min-w-tap px-5 text-base",
        elder: "min-h-tap-elder min-w-tap-elder px-7 text-2xl",
        icon: "min-h-tap min-w-tap",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp ref={ref} className={cn(buttonVariants({ variant, size }), className)} {...props} />
    );
  },
);
Button.displayName = "Button";
