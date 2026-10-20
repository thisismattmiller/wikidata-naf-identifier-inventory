-- Fetch data representations from inside a page in the crawler's Chrome window.
--   osascript browser_fetch.applescript <windowId> <pageUrl> <kickoffJs> <maxLoadSeconds> <maxFetchSeconds>
-- Loads <pageUrl> (empty = stay on the current page), runs <kickoffJs>, which starts the fetches and
-- fills window.__invFetch, then polls until window.__invFetch.done. Prints "<tab url>|<tab title>"
-- on the first line and JSON.stringify(window.__invFetch) after it.

on run argv
	set wid to item 1 of argv
	set pageUrl to item 2 of argv
	set kickoffJs to item 3 of argv
	set maxLoad to (item 4 of argv) as real
	set maxFetch to (item 5 of argv) as real

	tell application "Google Chrome"
		set t to active tab of window id wid
		if pageUrl is not "" then
			set URL of t to "about:blank"
			delay 0.3
			set URL of t to pageUrl
			delay 0.5
			set waited to 0.5
			repeat while ((loading of t) or (URL of t is "about:blank")) and waited < maxLoad
				delay 0.5
				set waited to waited + 0.5
			end repeat
			delay 1.5
		end if

		try
			execute t javascript kickoffJs
		on error errMsg
			return (URL of t) & "|" & (title of t) & linefeed & "{\"error\": \"kickoff failed\"}"
		end try

		set waited to 0
		set state to ""
		repeat while waited < maxFetch
			delay 1
			set waited to waited + 1
			try
				set state to (execute t javascript "window.__invFetch ? (window.__invFetch.done ? 'done' : 'running') : 'lost'") as text
			on error
				set state to "error"
			end try
			if state is "done" or state is "lost" then exit repeat
		end repeat

		try
			set r to (execute t javascript "JSON.stringify(window.__invFetch || {error: 'lost'})") as text
		on error
			set r to "{\"error\": \"could not read results\"}"
		end try
		return (URL of t) & "|" & (title of t) & linefeed & r
	end tell
end run
