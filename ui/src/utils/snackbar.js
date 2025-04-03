export const newErrorNotif = (text) => ({
    id: `error${+ new Date()}`,
    visible: true,
    text: text,
    color: 'error',
})

export const newSuccessNotif = (text, id) => ({
    id: id || `error${+ new Date()}`,
    visible: true,
    text: text,
    color: 'success',
})