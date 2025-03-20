const emailRe = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

export const loginAndRegisterRules = {
    notEmpty: value => value.length > 0,
    isEmail: value => emailRe.test(value),
}