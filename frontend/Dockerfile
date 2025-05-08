# Use Node image
FROM node:20

# Set working directory
WORKDIR /wiline_project

# Copy frontend code
COPY . .

# Install React dependencies
RUN npm install

# Expose frontend port
EXPOSE 3000

# Start the React dev server
CMD ["npm", "start"]
