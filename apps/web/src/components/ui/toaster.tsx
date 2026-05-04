"use client"

import * as Toast from "@radix-ui/react-toast"
import { create } from "zustand"

interface ToastState {
  open: boolean
  message: string
  variant: "default" | "success" | "error"
  show: (message: string, variant?: "default" | "success" | "error") => void
  hide: () => void
}

export const useToastStore = create<ToastState>((set) => ({
  open: false,
  message: "",
  variant: "default",
  show: (message, variant = "default") => set({ open: true, message, variant }),
  hide: () => set({ open: false }),
}))

export function Toaster() {
  const { open, message, variant, hide } = useToastStore()

  return (
    <Toast.Provider swipeDirection="right">
      <Toast.Root
        open={open}
        onOpenChange={(open) => { if (!open) hide() }}
        className={`rounded-lg border p-4 shadow-lg ${
          variant === "success" ? "bg-green-50 border-green-200" :
          variant === "error" ? "bg-red-50 border-red-200" :
          "bg-white border-gray-200"
        }`}
      >
        <Toast.Description className="text-sm">{message}</Toast.Description>
      </Toast.Root>
      <Toast.Viewport className="fixed bottom-4 right-4 flex flex-col gap-2 w-96" />
    </Toast.Provider>
  )
}
