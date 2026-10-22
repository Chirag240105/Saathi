import * as S from "@radix-ui/react-switch";
import type { ComponentProps } from "react";

export function Switch(props: ComponentProps<typeof S.Root>) {
  return (
    <S.Root
      className="relative h-8 w-14 shrink-0 rounded-full bg-sand-deep data-[state=checked]:bg-teal"
      {...props}
    >
      <S.Thumb className="block h-6 w-6 translate-x-1 rounded-full bg-white shadow transition-transform data-[state=checked]:translate-x-7" />
    </S.Root>
  );
}
