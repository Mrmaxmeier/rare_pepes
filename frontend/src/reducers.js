import { combineReducers } from 'redux'

const page = (state = 'home', action) => {
    switch (action.type) {
        case 'SET_PAGE':
            return action.page
        default:
            return state
    }
}

const queue = (state = [], action) => {
    switch (action.type) {
        case 'QUEUE_PUSH':
            return [
                ...state,
                action.item
            ]
        default:
            return state
    }
}

const voteStats = (votes = null, action) => {
    switch (action.type) {
        case 'INCR_VOTES':
            return votes + 1
        case 'SET_VOTES':
            return action.votes
        default:
            return votes
    }
}

const pepeCount = (pepeCount = null, action) => {
    switch (action.type) {
        case 'SET_PEPES':
            return action.pepeCount
        default:
            return pepeCount
    }
}

const stats = combineReducers({
    votes: voteStats,
    pepes: pepeCount
})

export const reducer = combineReducers({
    page,
    stats,
    queue
}) 