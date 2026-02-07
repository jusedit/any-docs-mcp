# Docs Authentication

*Documentation: E2E Test Documentation*

---

## Authentication

**Source:** http://127.0.0.1:12083/docs/authentication

# Authentication
AnyDocsMCP supports multiple authentication methods to secure your documentation server.
## API Key Authentication
The simplest method is using API keys. Generate a key and include it in the request header:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:3000/search?q=hooks
```
### Generating API Keys
Use the CLI to generate a new API key:
```dockerfile
from anydocs import auth
key = auth.generate_api_key(name="my-app", scopes=["read", "search"])
print(f"Your API key: {key.token}")
# Store this securely - it cannot be retrieved later
```
## OAuth2 Integration
For production environments, we recommend OAuth2 with PKCE flow:
```dockerfile
import { OAuth2Client } from 'anydocs-mcp/auth';
const oauth = new OAuth2Client({
  clientId: process.env.OAUTH_CLIENT_ID,
  redirectUri: 'http://localhost:3000/callback',
  scopes: ['docs:read', 'docs:search']
});
// Redirect user to authorization URL
const authUrl = oauth.getAuthorizationUrl();
console.log('Authorize at:', authUrl);
```
## JWT Token Validation
All authenticated requests use JWT tokens. The server validates tokens automatically:
```typescript
interface TokenPayload {
  sub: string;       // User ID
  scopes: string[];  // Granted permissions
  exp: number;       // Expiration timestamp
  iat: number;       // Issued at timestamp
}
```
Tokens expire after 24 hours by default. Use the refresh token to obtain a new access token without re-authentication.
## Troubleshooting Authentication
Common authentication errors and their solutions:
* **401 Unauthorized** - Check that your API key or token is valid and not expired
* **403 Forbidden** - Your token lacks the required scope for this operation
* **429 Too Many Requests** - You've exceeded the rate limit. Wait and retry.

---

