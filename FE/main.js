$(document).ready(function () {

   
    
    // Initialize text animation
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    let siriWave = null; // Store SiriWave instance

    // Initialize SiriWave (only once)
    function initializeSiriWave() {
        if (!siriWave) {
            siriWave = new SiriWave({
                container: document.getElementById("siri-container"),
                width: 800,
                height: 200,
                style: "ios9",
                amplitude: 1,
                speed: 0.3,
                autostart: true,
            });
        }
    }

    // Show SiriWave animation
    function showSiriWave() {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        initializeSiriWave();
    }

    // Handle Mic Button Click
    $("#MicBtn").click(function () {
        eel.playAssistantSound();
        showSiriWave();
        eel.allCommands()()
        eel.process_voice_command();
    });

    // Keyboard Event for "Ctrl + J"
    function doc_keyUp(e) {
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound();
            showSiriWave();
            eel.allCommands()()
            eel.process_voice_command();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // Play assistant function
    function PlayAssistant(message) {
        if (message !== "") {
            showSiriWave();
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Toggle mic and send button
    function ShowHideButton(message) {
        if (message.length === 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // Keyup event for chatbox
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // Send button click event
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    // Enter key event in chatbox
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });
});