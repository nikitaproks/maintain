FROM node:18-alpine as builder
RUN mkdir /frontend 
COPY . /frontend
RUN cd /frontend && npm install && npm run build


FROM node:18-alpine
RUN mkdir /frontend 
COPY --from=builder /frontend/build /frontend/build
COPY --from=builder /frontend/package.json /frontend/package-lock.json /frontend/
RUN cd /frontend && npm install --production
WORKDIR /frontend

CMD ["node", "build/index.js"]