# API Reference

Complete API documentation.

## Functions

### start(options)

Starts the server with given options.

**Parameters:**
- `options.port` (number): Port to listen on
- `options.host` (string): Host to bind to

**Example:**
```javascript
start({ port: 8080, host: '0.0.0.0' });
```

### stop()

Stops the running server.

## Events

### onConnect(callback)

Called when a client connects.

```javascript
onConnect((client) => {
  console.log('Client connected:', client.id);
});
```
