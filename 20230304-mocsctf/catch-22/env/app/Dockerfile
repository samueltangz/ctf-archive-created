FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock ./

COPY ./src ./src

RUN yarn install

ENV FLAG 'MOCSCTF{n0w_y0u_c4n_cl1p_thr0u9h}'

CMD ["yarn", "run", "dev"]
