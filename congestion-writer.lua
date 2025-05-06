obs           = obslua
temp_filepath = os.getenv("TEMP") .. "\\obs_status.txt"

function write_status()
    local success, err = pcall(function()
        local state = "offline"
        local congestion = 0.0

        local output = obs.obs_frontend_get_streaming_output()
        if output ~= nil then
            local active = obs.obs_output_active(output)
            local reconnecting = obs.obs_output_reconnecting(output)

            if active then
                if reconnecting then
                    state = "disconnected"
                    congestion = 1.0  -- treat as fully congested
                else
                    state = "online"
                    congestion = obs.obs_output_get_congestion(output) or 0.0
                end
            end

            obs.obs_output_release(output)
        end

        local file = io.open(temp_filepath, "w")
        if file then
            file:write(string.format("%.3f,%s", congestion, state))
            file:close()
        end
    end)

    if not success then
        obs.script_log(obs.LOG_WARNING, "write_status error: " .. tostring(err))
    end
end

function script_load(settings)
    obs.timer_add(write_status, 1000)
end

function script_unload()
    obs.timer_remove(write_status)
end

function script_description()
    return "Writes congestion and stream state to a temp file every second."
end