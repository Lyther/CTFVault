# syntax=docker/dockerfile:1
FROM golang:1.26.1-trixie AS build
WORKDIR /app
RUN --mount=type=cache,target=/go/pkg/mod/,sharing=locked \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=bind,source=go.mod,target=go.mod \
    go mod download -x
RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,target=. \
    CGO_ENABLED=1 go build -o /bin/server .

FROM debian:13.4-slim
WORKDIR /app
EXPOSE 80
COPY --from=build /bin/server /bin/
CMD ["/bin/server"]
