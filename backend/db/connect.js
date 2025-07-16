// server/db/connect.js
import mongoose from 'mongoose';
import dotenv from 'dotenv';

dotenv.config(); // Ensures environment variables are loaded

const connectDB = async () => {
  try {
    // Ensure you have MONGO_URI in your .env file
    // This line was previously commented out or missing the actual connection logic.
    await mongoose.connect(process.env.MONGO_URI, {
      // Mongoose 6 deprecated these options, but keep them if you're on Mongoose 5 or earlier
      // useNewUrlParser: true, // No longer needed in Mongoose 6+
      // useUnifiedTopology: true, // No longer needed in Mongoose 6+
      // useCreateIndex: true, // No longer needed in Mongoose 6+
      // useFindAndModify: false, // No longer needed in Mongoose 6+
    });
    console.log('💾 MongoDB Connected Successfully!'); // Confirmation message
  } catch (error) {
    console.error('❌ MongoDB Connection Error:', error.message);
    // Exit process with failure if DB connection fails
    process.exit(1);
  }
};

export default connectDB;