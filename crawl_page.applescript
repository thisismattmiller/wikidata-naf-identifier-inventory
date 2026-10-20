-- Load one URL in the crawler's Chrome window, wait for it to render, run the extraction JS.
--   osascript crawl_page.applescript <windowId> <url> <prefetchJs> <extractJs> <maxLoadSeconds> <maxSettleSeconds>
-- An empty <url> skips navigation and re-harvests whatever the tab currently shows.
-- Prints "<loadTimedOut>|<tab url>|<tab title>" on the first line, then the JSON from extract.js.
-- Requires Chrome > View > Developer > "Allow JavaScript from Apple Events".

on run argv
	set wid to item 1 of argv -- Chrome window ids are text; as integers the large ones get mangled
	set theURL to item 2 of argv
	set prefetchJs to item 3 of argv
	set extractJs to item 4 of argv
	set maxLoad to (item 5 of argv) as real
	set maxSettle to (item 6 of argv) as real
	set timedOut to false

	tell application "Google Chrome"
		set t to active tab of window id wid

		if theURL is not "" then
			-- blank the tab first so a failed navigation can never be mistaken for the previous page
			set URL of t to "about:blank"
			delay 0.3
			set URL of t to theURL
			delay 0.5
			set waited to 0.5
			repeat while ((loading of t) or (URL of t is "about:blank")) and waited < maxLoad
				delay 0.5
				set waited to waited + 0.5
			end repeat
			if waited ≥ maxLoad then set timedOut to true
		end if
		try
			execute t javascript prefetchJs
		end try

		-- wait for client-side rendering to stop changing the DOM
		set lastState to ""
		set stableCount to 0
		set settled to 0
		repeat while stableCount < 2 and settled < maxSettle
			delay 0.75
			set settled to settled + 0.75
			try
				set curState to (execute t javascript "document.documentElement.outerHTML.length + '|' + document.title + '|' + location.href") as text
			on error
				set curState to "error"
			end try
			if curState is equal to lastState then
				set stableCount to stableCount + 1
			else
				set stableCount to 0
			end if
			set lastState to curState
		end repeat

		set tabURL to URL of t
		set tabTitle to title of t
		try
			set r to (execute t javascript extractJs) as text
		on error errMsg
			set r to "{\"extract_error\": \"execute javascript failed\"}"
		end try
		return (timedOut as text) & "|" & tabURL & "|" & tabTitle & linefeed & r
	end tell
end run
