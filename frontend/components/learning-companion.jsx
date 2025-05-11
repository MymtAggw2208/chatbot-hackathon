"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar } from "@/components/ui/avatar"
import { Lightbulb, MessageCircle, Send, ThumbsUp } from "lucide-react"
import { cn } from "@/lib/utils"

export function LearningCompanion() {
  const [hintMessages, setHintMessages] = useState([
    {
      id: "welcome-hint",
      content: "こんにちは、何でも聞いてね！ヒントを教えてあげるよ！",
      sender: "ai",
      type: "feedback",
    },
  ])
  const [explanationMessages, setExplanationMessages] = useState([
    {
      id: "welcome-expl",
      content: "こんにちは！説明が必要なら、質問してね！",
      sender: "ai",
      type: "feedback",
    },
  ])
  const [input, setInput] = useState("")
  const [mode, setMode] = useState("hint")
  const [isThinking, setIsThinking] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    scrollToBottom()
  }, [hintMessages, explanationMessages, mode])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = {
      id: Date.now().toString(),
      content: input,
      sender: "user",
      type: mode,
    }

    const isHint = mode === "hint"
    const setTargetMessages = isHint ? setHintMessages : setExplanationMessages
    const getTargetMessages = isHint ? hintMessages : explanationMessages
    const endpoint = isHint ? "/chat/thinking" : "/chat/answer"

    setTargetMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsThinking(true)

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input, history: [] }),
      })
      const data = await res.json()
      const aiMessage = {
        id: Date.now().toString(),
        content: data.response,
        sender: "ai",
        type: "feedback",
      }
      setTargetMessages((prev) => [...prev, aiMessage])
    } catch (error) {
      console.error("Error fetching AI response:", error)
    } finally {
      setIsThinking(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleFeedback = () => {
    const feedbackMessage = {
      id: Date.now().toString(),
      content: "すごい！自分で考えて答えを見つけられたね。その考え方はとても良いよ！次の問題にも挑戦してみよう！",
      sender: "ai",
      type: "feedback",
    }

    if (mode === "hint") {
      setHintMessages((prev) => [...prev, feedbackMessage])
    } else {
      setExplanationMessages((prev) => [...prev, feedbackMessage])
    }
  }

  const currentMessages = mode === "hint" ? hintMessages : explanationMessages

  return (
    <div className="flex flex-col w-full max-w-4xl mx-auto h-[calc(100vh-2rem)]">
      {/* ヘッダー */}
      <div className="flex-none">
        <Tabs defaultValue="hint" className="w-full" onValueChange={(value) => setMode(value)}>
          <TabsList className="grid w-full grid-cols-2 bg-amber-100">
            <TabsTrigger value="hint" className="data-[state=active]:bg-orange-200 flex justify-center items-center">
              <Lightbulb className="mr-2 h-4 w-4" />
              ヒントモード
            </TabsTrigger>
            <TabsTrigger value="explanation" className="data-[state=active]:bg-orange-200 flex justify-center items-center">
              <MessageCircle className="mr-2 h-4 w-4" />
              説明モード
            </TabsTrigger>
          </TabsList>
          <TabsContent value="hint" className="mt-2">
            <Card className="border-amber-200">
              <CardContent className="pt-4 bg-amber-50">
                <p>
                   ヒントモードでは、答えをそのまま教えるのではなく、考え方のヒントを教えてくれます。
                  ラーニーちゃんと一緒に考えて答えを見つけよう！
                </p>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="explanation" className="mt-2">
            <Card className="border-amber-200">
              <CardContent className="pt-4 bg-amber-50">
                  <p>説明モードでは、質問に対してあなたの考えを説明してもらいます。
                  ラーニーちゃんに説明して、理解を深めよう！</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* チャット表示 */}
      <div className="flex-grow overflow-y-auto p-4 space-y-4 my-4">
        {currentMessages.map((message, index) => (
          <div key={message.id || index} className={cn("flex", message.sender === "user" ? "justify-end" : "justify-start")}>
            <div
              className={cn(
                "max-w-[80%] rounded-lg p-3",
                message.sender === "user" ? "bg-orange-500 text-white" : "bg-gray-100",
                message.type === "hint" && "bg-amber-100",
                message.type === "explanation" && "bg-yellow-100",
                message.type === "feedback" && "bg-orange-100",
              )}
            >
              {message.sender === "ai" && (
                <div className="flex items-center mb-1">
                  <Avatar className="h-6 w-6 mr-2">
                      <img src="/path/to/default.svg" alt="AI Icon" className="h-full w-full object-cover" />
                  </Avatar>
                  <span className="text-xs font-medium">
                    {message.type === "hint" && "ヒント"}
                    {message.type === "explanation" && "説明を聞かせて"}
                    {message.type === "feedback" && "フィードバック"}
                  </span>
                </div>
              )}
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* 入力欄 */}
      <div className="flex-none p-4 bg-white border-t border-amber-200">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="ラーニーちゃんに質問してみよう！"
            className="flex-1"
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="rounded-full bg-orange-500 hover:bg-orange-600"
          >
            <Send className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            onClick={handleFeedback}
            title="答えが分かったらクリック"
            className="rounded-full border-orange-300 text-orange-700 hover:bg-orange-100"
          >
            <ThumbsUp className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
