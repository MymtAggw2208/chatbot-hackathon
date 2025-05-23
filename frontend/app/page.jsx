import { LearningCompanion } from "@/components/learning-companion"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-2 md:p-4">
      <div className="z-10 w-full max-w-5xl flex flex-col h-full">
        <h1 className="text-xl md:text-3xl font-bold text-center my-4 text-orange-600">
          学びのお友達 ラーニーちゃんと一緒に考えよう！
        </h1>
        <LearningCompanion />
      </div>
    </main>
  )
}
