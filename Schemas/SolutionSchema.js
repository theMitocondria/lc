import mongoose from "mongoose";

const SolutionSchema = new mongoose.Schema({
    rank : {type : Number, unique : true},
    Solution : {type : String},

})

const Solutions = new mongoose.model('Contest', SolutionSchema)
export default Solutions;