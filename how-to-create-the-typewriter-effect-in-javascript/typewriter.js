const typeText = async (id, text) => {
    let typedText = ''
    let delay = 75
    while (text.length >= typedText.length) {
        $(id).text(typedText)
        await new Promise(res => setTimeout(res, delay))
        typedText += text[typedText.length]
    }
}

const untypeText = async (id, text) => {
    let typedText = text
    let delay = 75
    while (typedText.length > 0) {
        $(id).text(typedText)
        await new Promise(res => setTimeout(res, delay))
        typedText = typedText.substring(0, typedText.length - 1)
    }
}

$(document).ready(async () => {
    let typewriterText = [
        'software engineer.',
        'guac lover.',
        'boba drinker.',
        'corgi snuggler.'
    ]
    let index = 0
    do {
        await typeText('#typewriter-text', typewriterText[index])
        await new Promise(res => setTimeout(res, 3*1000));
        await untypeText('#typewriter-text', typewriterText[index])
        index += 1
        index = index % typewriterText.length
    } while (true)
})
