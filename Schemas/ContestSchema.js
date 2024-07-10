import mongoose from "mongoose";

const ContestSchema = new mongoose.Schema({
    name : {type : String},
    question3 : {type : Array},
    question4 : {type : Array},

})

const Contest = new mongoose.model('Contest', ContestSchema)
export default Contest;