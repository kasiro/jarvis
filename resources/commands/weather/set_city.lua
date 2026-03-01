-- set city for weather command

local phrase = jarvis.context.phrase
local lang = jarvis.context.language

-- Default city: Novosibirsk
local city = "Novosibirsk"

-- try to extract city name from phrase if provided
local extracted_city = phrase:match("город%s+(.+)") or phrase:match("city%s+(.+)")

if extracted_city then
    city = extracted_city:gsub("^%s*(.-)%s*$", "%1") -- trim
end

-- save to state (shared with weather command)
jarvis.state.set("city", city)

local msg = lang == "ru"
    and "Город установлен: " .. city
    or "City set to: " .. city

jarvis.log("info", msg)
jarvis.system.notify("Jarvis", msg)
jarvis.audio.play_ok()

return { chain = false }