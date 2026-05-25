#Requires AutoHotkey v2.0
#SingleInstance Force
SetKeyDelay -1, -1

; =========================
; STATE
; =========================
global running := false
global paused := false

global stepIndex := 1
global stepRemaining := 0.0
global currentKeys := []

global startTime := 0
global lastReset := 0
global targetExe := ""

; =========================
; CONFIG
; =========================
global BASE := [58.0, 2.0, 58.0, 2.0]
global STEP_KEYS := [
    ["a","r"],
    ["w"],
    ["r","d"],
    ["w"]
]

; =========================
; GUI
; =========================
ui := Gui("+AlwaysOnTop +Resize +MinSize240x200", "Automation Panel")
ui.BackColor := "0x0f1419"
ui.SetFont("s9", "Segoe UI")

statusTxt  := ui.AddText("xm ym cFFFFFF w220", "STOPPED")
runtimeTxt := ui.AddText("xm cAAAAAA w220", "00:00")

ui.AddText("xm cCCCCCC", "Keys:")
keysTxt := ui.AddText("xm cFFFFFF w220", "-")

ui.AddText("xm cCCCCCC", "Step:")
stepTxt := ui.AddText("xm cFFFFFF w220", "-")

ui.AddText("xm cCCCCCC", "Remaining:")
remainTxt := ui.AddText("xm cFFFFFF w220", "-")

ui.AddText("xm cAAAAAA", "Target App:")
ddl := ui.AddDropDownList("xm w220")

confirmBtn := ui.AddButton("xm w220", "Confirm Target")
refreshBtn := ui.AddButton("xm w220", "Refresh List")

ui.Show("x0 y0 w260 h260")

; =========================
; WINDOW LIST
; =========================
RefreshWindows(*) {
    global ddl
    ddl.Delete()
    seen := Map()

    for hwnd in WinGetList() {
        exe := WinGetProcessName(hwnd)
        if (exe != "" && !seen.Has(exe)) {
            ddl.Add([exe])
            seen[exe] := true
        }
    }
}

SelectTarget(*) {
    global ddl, targetExe
    targetExe := ddl.Text
    ToolTip "Target: " targetExe, 10, 10
    SetTimer(() => ToolTip(), -1000)
}

refreshBtn.OnEvent("Click", RefreshWindows)
confirmBtn.OnEvent("Click", SelectTarget)

RefreshWindows()

; =========================
; HELPERS
; =========================
RandDuration(base) {
    return base + Random(0.0, 0.5)
}

SendToTarget(keys, down := true) {
    global targetExe

    ; Try background send first
    for k in keys {
        if down
            ControlSend "{" k " down}", , "ahk_exe " targetExe
        else
            ControlSend "{" k " up}", , "ahk_exe " targetExe
    }
}

ReleaseAll() {
    SendToTarget(["a","r","d","w","z"], false)
}

TapZ() {
    ControlSend "{z}", , "ahk_exe " targetExe
}

FormatTime(ms) {
    total := Floor(ms / 1000)
    return Format("{:02}:{:02}", Floor(total/60), Mod(total,60))
}

StrJoin(arr, sep) {
    out := ""
    for i, v in arr
        out .= (i=1 ? "" : sep) v
    return out
}

; =========================
; UI UPDATE
; =========================
UpdateUI() {
    global running, paused, startTime
    global stepIndex, stepRemaining, currentKeys

    statusTxt.Text := running ? (paused ? "PAUSED" : "RUNNING") : "STOPPED"

    if running
        runtimeTxt.Text := FormatTime(A_TickCount - startTime)

    keysTxt.Text := currentKeys.Length ? StrJoin(currentKeys, " + ") : "-"
    stepTxt.Text := stepIndex
    remainTxt.Text := Round(stepRemaining, 2) "s"
}

; =========================
; MAIN LOOP
; =========================
MainLoop() {
    global running, paused
    global stepIndex, stepRemaining, currentKeys
    global lastReset

    static lastTick := 0

    if !running {
        SetTimer(MainLoop, 0)
        ReleaseAll()
        lastTick := 0
        return
    }

    if (lastTick = 0)
        lastTick := A_TickCount

    now := A_TickCount
    dt := (now - lastTick) / 1000.0
    lastTick := now

    if paused {
        SendToTarget(currentKeys, false)
        UpdateUI()
        return
    }

    if (now - lastReset >= 900000) {
        SendToTarget(currentKeys, false)
        TapZ()

        stepIndex := 1
        stepRemaining := 0
        currentKeys := []
        lastReset := now
        UpdateUI()
        return
    }

    if (stepRemaining <= 0) {
        stepRemaining := RandDuration(BASE[stepIndex])
        currentKeys := STEP_KEYS[stepIndex]
        SendToTarget(currentKeys, true)
    }

    stepRemaining -= dt

    if (stepRemaining <= 0) {
        SendToTarget(currentKeys, false)
        stepIndex := Mod(stepIndex, 4) + 1
        stepRemaining := 0
    }

    UpdateUI()
}

; =========================
; HOTKEYS — ONLY WHEN TARGET WINDOW IS ACTIVE
; =========================
#HotIf (targetExe != "" && WinActive("ahk_exe " targetExe))

\:: {
    global running, paused, startTime, lastReset

    if running {
        running := false
        ToolTip "STOPPED", 10, 10
        SetTimer(() => ToolTip(), -800)
        return
    }

    running := true
    paused := false
    startTime := A_TickCount
    lastReset := A_TickCount

    ToolTip "RUNNING", 10, 10
    SetTimer(() => ToolTip(), -800)

    SetTimer(MainLoop, 5)
}

]:: {
    global paused, running
    if running
        paused := !paused
}

NumpadSub:: {
    running := false
    paused := false
    ReleaseAll()
}

#HotIf