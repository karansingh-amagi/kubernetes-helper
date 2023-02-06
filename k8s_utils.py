from kubernetes import client, config, utils, dynamic
from kubernetes.client import api_client
import json
import os
import datetime


class K8sHelper:
    def __init__(self) -> None:
        ### Do we need context? ###
        # config.load_kube_config(context)
        config.load_kube_config(
            config_file=os.environ.get("KUBECONFIG"),
            context=os.environ.get("KUBECONTEXT"),
        )
        self.v1core = client.CoreV1Api()
        self.v1apps = client.AppsV1Api()
        self.api = client.ApiClient()
        self.dynamic_client = dynamic.DynamicClient(
            api_client.ApiClient()
        )

    ################### Pods ####################

    def pods_status_all_namespaces(self) -> json:
        data = self.v1core.list_pod_for_all_namespaces(watch=False)
        pod_data = []
        for pod in data.items:
            pod_data.append({
                "pod_name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "phase": pod.status.phase,
                "pod_ip": pod.status.pod_ip,
                "start_time": pod.status.start_time,
                "containers": [{
                    "container_image": pod.status.container_statuses[i].image,
                    "name": pod.status.container_statuses[i].name,
                    "ready_status": pod.status.container_statuses[i].ready,
                    "started_status": pod.status.container_statuses[i].started,
                    "state": pod.status.container_statuses[i].state
                } for i in range(len(pod.status.container_statuses))]
            })

        pod_data = json.dumps(pod_data, indent=4, default=str)
        return pod_data

    def pods_status_namespace(self, namespace: str) -> json:
        # Todo: Logger
        print("Retrieving status of pods in {} namespace".format(namespace))

        pod_data = json.loads(self.pods_status_all_namespaces())
        pod_data_ns = []
        for pod in pod_data:
            if pod["namespace"] == namespace:
                pod_data_ns.append(pod)

        return json.dumps(pod_data_ns, indent=4, default=str)

    def delete_pod(self, name: str, namespace: str = "default"):
        # Todo: Logger
        print("Deleting pod {}.{}".format(name, namespace))
        try:
            # Todo: Handle delete body options
            resp = self.v1core.delete_namespaced_pod(
                name=name, namespace=namespace, body=client.V1DeleteOptions())
            return resp

        except Exception as e:
            return e

    ##################################################

    ################### Deployment ####################

    ### Do we need deployment status/replicas? ###
    def deployment_status(self):
        data = self.v1apps.list_deployment_for_all_namespaces()

        # Will prune data as per requirement post discussion
        return data

    def deployment_rollout_restart(self, name: str, namespace: str = "default"):
        # Todo: Logger
        print("Starting rollout restart for deployment {}.{}".format(name, namespace))

        api = self.dynamic_client.resources.get(
            api_version="apps/v1", kind="Deployment")
        body = {
            'spec': {
                'template': {
                    'metadata': {
                        'annotations': {
                            'kubectl.kubernetes.io/restartedAt': datetime.datetime.utcnow()
                        }
                    }
                }
            }
        }

        try:
            resp = api.patch(
                body=body, name=name, namespace=namespace
            )
            return e
        except Exception as e:
            return e

    def delete_deployment(self, name: str, namespace: str = "default"):
        # Todo: Logger
        print("Deleting deployment {}.{}".format(name, namespace))

        try:
            # Todo: Handle delete body options
            resp = self.v1apps.delete_namespaced_deployment(
                name=name,
                namespace=namespace,
                body=client.V1DeleteOptions(),
            )
            # Todo: prune return data
            return resp

        except Exception as e:
            return e

    def apply_from_file(self, yaml_file: str):
        # Todo: Logger
        print("Applying configuration from file at {}".format(yaml_file))

        try:
            resp = utils.create_from_yaml(self.api, yaml_file, verbose=True)
            # Todo: prune return data
            return resp
        except Exception as e:
            return e

    def apply_from_directory(self, yaml_dir):
        # Todo: Logger
        print("Applying configuration from files at {}".format(yaml_dir))

        try:
            resp = utils.create_from_directory(
                self.api, yaml_dir, verbose=True)
            # Todo: prune return data
            return resp
        except Exception as e:
            return e

    ##################################################

    ################### Service ####################
    def services_status(self):
        data = self.v1core.list_service_for_all_namespaces()

        # Will prune data as per requirement post discussion
        return data


k8s = K8sHelper()
ret = k8s.pods_status_all_namespaces()
# k8s.delete_pod("pi-t2854")
# ret = k8s.pods_status_namespace("default")
# ret = k8s.depl_status()
# ret = k8s.apply_from_file("nginx-deployment.yaml")
# ret = k8s.delete_deployment("nginx-deployment")
# ret = k8s.deployment_status()
# ret = k8s.rolling_restart('mongo-express')
print(ret)
