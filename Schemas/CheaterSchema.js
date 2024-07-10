import mongoose from "mongoose";

const CheaterSchema = new mongoose.Schema({
    userName : {type : String, unique : true},
    rank : {type : Number, unique : true},
    questionLink : {type : String},

})

const Cheaters = new mongoose.model('Contest', CheaterSchema)
export default Cheaters;