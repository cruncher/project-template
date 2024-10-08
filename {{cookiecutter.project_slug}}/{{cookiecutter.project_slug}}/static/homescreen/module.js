
/*
Handle install prompt on Desktop Chrome, Brave and Android Chrome, Brave,
Firefox. Requires a service worker with a fetch handler to be installed.
*/

const button = document.getElementById('homescreen-button');

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();

    // Stash the event so it can be triggered later.
    let deferredPrompt = e;

    // Update UI to notify the user they can add to home screen
    button.hidden = false;

    button.addEventListener('click', (e) => {
        // Show the prompt
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the A2HS prompt');
                // hide our user interface that shows our A2HS button
                // Why doesn't it do this?
                button.hidden = true;

                setTimeout(function() {
                    // Does it do this?
                    button.hidden = true;
                }, 300);
            }
            else {
                console.log('User dismissed the A2HS prompt');
            }

            deferredPrompt = null;
        });
    });
});

window.addEventListener('appinstalled', (evt) => {
    console.log('Installed on Home Screen');
});
