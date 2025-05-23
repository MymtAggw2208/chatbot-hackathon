"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Lightbulb, MessageCircle, Send, ThumbsUp } from "lucide-react"
import { cn } from "@/lib/utils"
import { Textarea } from "@/components/ui/textarea"

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
      content: "こんにちは！この前学習したこと覚えているかな？\n今からどれくらい覚えているかラーニーと一緒にチェックしてみよう！",
      sender: "ai",
      type: "feedback",
    },
  ])
  const [input, setInput] = useState("")
  const [mode, setMode] = useState("hint")
  const [isThinking, setIsThinking] = useState(false)
  const [hintConversationId, setHintConversationId] = useState(null)
  const [explanationConversationId, setExplanationConversationId] = useState(null)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    scrollToBottom()
  }, [hintMessages, explanationMessages, mode])

  useEffect(() => {
    adjustTextareaHeight()
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current
    if (!textarea) return

    textarea.style.height = "auto"
    const scrollHeight = textarea.scrollHeight

    const lineHeight = 24
    const maxHeight = lineHeight * 4 + 16

    textarea.style.height = `${Math.min(scrollHeight, maxHeight)}px`
  }

  const handleSend = async () => {
    if (!input.trim() || isThinking) return  // ← 二重送信防止

    const userMessage = {
      id: Date.now().toString(),
      content: input,
      sender: "user",
      type: mode,
    }

    const isHint = mode === "hint"
    const setTargetMessages = isHint ? setHintMessages : setExplanationMessages
    const getTargetMessages = isHint ? hintMessages : explanationMessages
    const endpoint = isHint ? "/chat/thinking" : "/chat/understanding_evaluation"
    const conversationId = isHint ? hintConversationId : explanationConversationId

    setTargetMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsThinking(true)

    const requestBody = {
      question: input,
      history: buildHistory(getTargetMessages),
      conversation_id: conversationId,
    }

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      })

      if (!res.ok) throw new Error(`API request failed with status ${res.status}`)

      const data = await res.json()

      const aiMessage = {
        id: Date.now().toString(),
        content: data.response,
        sender: "ai",
        type: mode,
      }

      setTargetMessages((prev) => [...prev, aiMessage])

      if (isHint && !hintConversationId && data.conversation_id) {
        setHintConversationId(data.conversation_id)
      }
      if (!isHint && !explanationConversationId && data.conversation_id) {
        setExplanationConversationId(data.conversation_id)
      }

    } catch (error) {
      console.error("Error fetching AI response:", error)
    } finally {
      setIsThinking(false)
    }
  }

  const buildHistory = (messages) => {
    return messages
      .filter((msg) => msg.type !== "feedback")
      .map((msg) => ({
        role: msg.sender === "user" ? "user" : "assistant",
        content: msg.content,
      }))
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !isThinking) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleInputChange = (e) => {
    setInput(e.target.value)
    adjustTextareaHeight()
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
    <div className="flex flex-col w-full max-w-5xl mx-auto h-[calc(100vh-2rem)] text-lg">
      {/* ヘッダー - 固定表示 */}
      <div className="sticky top-0 z-10 bg-white">
        <Tabs defaultValue="hint" className="w-full" onValueChange={(value) => setMode(value)}>
          <TabsList className="grid w-full grid-cols-2 p-0 h-auto">
            <TabsTrigger 
              value="hint" 
              className="bg-orange-200 data-[state=active]:bg-orange-300 flex justify-center items-center py-4 h-full rounded-none"
            >
              <Lightbulb className="mr-3 h-10 w-10" />
              ヒントモード
            </TabsTrigger>
            <TabsTrigger 
              value="explanation" 
              className="bg-orange-200 data-[state=active]:bg-orange-300 flex justify-center items-center py-4 h-full rounded-none"
              onClick={() => console.log('タブがクリックされました')}
            >
              <MessageCircle className="mr-3 h-10 w-10" />
              理解度チェックモード
            </TabsTrigger>
          </TabsList>
          <TabsContent value="hint" className="mt-2">
            <Card className="border-amber-200">
              <CardContent className="p-4 bg-amber-50">
                <p className="whitespace-pre-line text-left">
                  ヒントモードでは、答えをそのまま教えるのではなく、考え方のヒントを教えてくれます。
                  <br />ラーニーちゃんと一緒に考えて答えを見つけよう！
                </p>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="explanation" className="mt-2">
            <Card className="border-amber-200">
              <CardContent className="p-4 bg-amber-50">
                <p className="whitespace-pre-line text-left">
                  理解度チェックモードでは、ヒントモードで学習した内容をどれくらい分かっているかチェックできます。
                  <br />ラーニーちゃんにどうやって答えが出たのか説明して、理解度をチェックして更に理解を深めよう！
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* チャット表示 - スクロール可能領域 */}
      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {currentMessages.map((message, index) => (
          <div key={message.id || index} className={cn("flex", message.sender === "user" ? "justify-end" : "justify-start")}>
            <div
              className={cn(
                "max-w-[80%] rounded-lg p-3",
                message.sender === "user" ? "bg-orange-500 text-black" : "bg-gray-100",
                message.type === "hint" && "bg-amber-100",
                message.type === "explanation" && "bg-yellow-100",
                message.type === "feedback" && "bg-orange-100",
              )}
            >
              {message.sender === "ai" && (
                <div className="flex items-center mb-1">
                  <Avatar className="h-12 w-12 mr-3">
                    <AvatarImage src="/default.png" alt="AI Icon" />
                    <AvatarFallback>AI</AvatarFallback>
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

      {/* 入力欄 - 固定表示 */}
      <div className="sticky bottom-0 z-10 bg-white border-t border-amber-200">
        <div className="flex gap-2 p-4">
          <Textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === "Enter" && e.ctrlKey) {
                e.preventDefault()
                handleSend()
              }
            }}
            placeholder="ラーニーちゃんに質問してみよう！"
            className="flex-1 min-h-[40px] max-h-[120px] resize-none py-2 px-3"
            rows={1}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="rounded-full bg-orange-500 hover:bg-orange-600 p-3 self-end flex items-center justify-center"
          >
            <Send className="h-6 w-6" />
          </Button>
          <Button
            variant="outline" 
            onClick={handleFeedback}
            title="答えが分かったらクリック"
            className="rounded-full border-orange-300 text-orange-700 hover:bg-orange-100 self-end flex items-center justify-center"
          >
            <ThumbsUp className="h-6 w-6" />
          </Button>
        </div>
      </div>
    </div>
  )
}
