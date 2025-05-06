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
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      content: "こんにちは！何か質問があれば、聞いてね！",
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
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = {
      id: Date.now().toString(),
      content: input,
      sender: "user",
      type: "question",
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsThinking(true)

    // Simulate AI thinking time
    setTimeout(() => {
      let response

      if (mode === "hint") {
        response = {
          id: (Date.now() + 1).toString(),
          content: generateHint(input),
          sender: "ai",
          type: "hint",
        }
      } else {
        response = {
          id: (Date.now() + 1).toString(),
          content: generateExplanationPrompt(input),
          sender: "ai",
          type: "explanation",
        }
      }

      setMessages((prev) => [...prev, response])
      setIsThinking(false)
    }, 1500)
  }

  const generateHint = (question) => {
    // This would be replaced with actual AI logic
    if (question.includes("計算") || question.includes("数学")) {
      return "その計算問題を解くには、まず何が分かっていて、何を求めればいいのかを整理してみよう。どんな公式が使えそうかな？"
    } else if (question.includes("歴史") || question.includes("いつ")) {
      return "歴史の出来事を考えるときは、その時代の背景や前後の出来事を思い出すと良いよ。何か関連する出来事を知っているかな？"
    } else if (question.includes("理科") || question.includes("なぜ")) {
      return "その現象の原因を考えるときは、似たような例を思い出してみよう。どんな法則が関係していると思う？"
    } else {
      return "その問題について、まず知っていることをノートに書き出してみよう。それから、どうやって解決できるか考えてみよう。何か思いついたことはある？"
    }
  }

  const generateExplanationPrompt = (question) => {
    return `「${question}」について、あなたはどう考えますか？あなたの言葉で説明してみてください。`
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
    setMessages((prev) => [...prev, feedbackMessage])
  }

  return (
    <div className="flex flex-col w-full max-w-4xl mx-auto h-[calc(100vh-2rem)]">
      {/* ヘッダー部分（固定） */}
      <div className="flex-none">
        <Tabs defaultValue="hint" className="w-full" onValueChange={(value) => setMode(value)}>
          <TabsList className="grid w-full grid-cols-2 bg-amber-100">
            <TabsTrigger value="hint" className="data-[state=active]:bg-orange-200">
              <Lightbulb className="mr-2 h-4 w-4" />
              ヒントモード
            </TabsTrigger>
            <TabsTrigger value="explanation" className="data-[state=active]:bg-orange-200">
              <MessageCircle className="mr-2 h-4 w-4" />
              説明モード
            </TabsTrigger>
          </TabsList>
          <TabsContent value="hint" className="mt-2">
            <Card className="border-amber-200">
              <CardContent className="pt-4 bg-amber-50">
                <p>
                  ヒントモードでは、答えをそのまま教えるのではなく、考え方のヒントを提供します。自分で考えて答えを見つけましょう！
                </p>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="explanation" className="mt-2">
            <Card className="border-amber-200">
              <CardContent className="pt-4 bg-amber-50">
                <p>説明モードでは、質問に対してあなたの考えを説明してもらいます。説明することで理解が深まります！</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* チャット内容部分（スクロール可能） */}
      <div className="flex-grow overflow-y-auto p-4 space-y-4 my-4">
        {messages.map((message) => (
          <div key={message.id} className={cn("flex", message.sender === "user" ? "justify-end" : "justify-start")}>
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
                    <div className="bg-amber-300 h-full w-full flex items-center justify-center">AI</div>
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

      {/* チャット入力部分（固定） */}
      <div className="flex-none p-4 bg-white border-t border-amber-200">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="質問を入力してください..."
            className="flex-1"
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="bg-orange-500 hover:bg-orange-600"
          >
            <Send className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            onClick={handleFeedback}
            title="答えが分かったらクリック"
            className="border-orange-300 text-orange-700 hover:bg-orange-100"
          >
            <ThumbsUp className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
