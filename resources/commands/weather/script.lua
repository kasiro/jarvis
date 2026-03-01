-- weather command using wttr.in API

local lang = jarvis.context.language

-- get saved city or use default
local city = jarvis.state.get("city") or "Novosibirsk"

jarvis.log("info", "Fetching weather for: " .. city)

-- Try wttr.in API with different formats
local url = "http://wttr.in/" .. city .. "?format=3&lang=" .. lang
local response = jarvis.http.get(url)

if response.ok and response.body and #response.body > 0 then
    jarvis.log("info", "Weather (wttr.in): " .. response.body)

    -- show notification
    local title = lang == "ru" and "Погода" or "Weather"
    jarvis.system.notify(title, response.body)
    jarvis.audio.play_ok()
    return { chain = false }
end

-- Both methods failed
jarvis.log("error", "Failed to fetch weather: wttr.in failed")
jarvis.audio.play_error()

return { chain = false }
