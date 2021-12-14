// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

const { url, port } = {
  url: 'http://10.100.2.20', // API Test
  port: '8080'
};

export const environment = {
  production: false,
  API_URL: url,
  API_PORT: port,
  API_HOST: `${url}${port ? `:${port}` : ''}`
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
